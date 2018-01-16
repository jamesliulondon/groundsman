from  modules.uri_tools import Uri_tools
from  modules.config_tools import Collect_configs
from  modules.time_tools import Time_tools



search_root = 'patterns'
config_file_type = '*.json'
elastic_host = 'londeldev01-n1.systems.london.cantor.com'
e_user='elastic'
e_pass='changeme'
pattern_interval = 7




def main():
    """
    'threshold' will be the watcher json posted.
    """
    config_tools = Collect_configs()
    U = Uri_tools()
    time_tools = Time_tools()
    file_list = config_tools.collect_config_files(search_root)


    for found_file in file_list:
        print "working with: " + found_file

        path=search_root + '/' + found_file.replace('./', '')
        watcher = (found_file.split('/')[-1]).replace('.json','')
        print "Watch: " + watcher
        print "Path: " + path
        
        loaded_data = config_tools.read_json(path)
        threshold, schedule = config_tools.split_config(loaded_data)
        sensitivity = config_tools.get_sensitivity(schedule)
        sliding_window = config_tools.get_windowsize(schedule)

        
        
        
        timerange=time_tools.get_timecode(7,sliding_window)
        json_timerange=time_tools.constuct_queryjson(timerange)
        index = config_tools.get_index(threshold)
        indexdoctype=config_tools.get_indexdoctype(schedule)
        #print "QUERY : " + json.dumps(json_timerange)
        tminus1 = U.connect_elastic(elastic_host,e_user,e_pass,index,indexdoctype,json_timerange)
        print "TMINUS1"
        print tminus1


        print "schedule" + str(schedule)
        sensitivity = config_tools.get_sensitivity(schedule)
        trigger_count = (int (tminus1['count']) * sensitivity)/100
        print "trigger_count:" + str(trigger_count)
        print "sensitivity: " + str(sensitivity)
        print "threshold: " + str(threshold)

        print "THRESHOLD: " + str(threshold)
        threshold['condition']['compare']['ctx.payload.hits.total']['lte'] = trigger_count
        print ""
        print "THRESHOLD: " + str(threshold)

        new_threshold = time_tools.construct_threshold_message(threshold,schedule,trigger_count)
        threshold_w_window = time_tools.construct_insertion_time_gte_threshold_message(new_threshold,schedule)
        #new_threshold = time_tools.construct_insertion_time_lte_threshold_message(new_threshold,schedule)
        
        print threshold_w_window
        U.disarm_elastic_threshold(elastic_host,e_user,e_pass,watcher,threshold_w_window)
        if int(trigger_count) < 1:
            U.arm_elastic_threshold(elastic_host,e_user,e_pass,watcher,threshold_w_window)


if __name__=='__main__':
    main()