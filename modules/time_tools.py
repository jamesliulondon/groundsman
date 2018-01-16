import datetime as DT
import json

class Time_tools():
    
    def get_timecode(self, days, window):
        """ Nearest Minutes Ago """
        today = DT.datetime.now()
        days_ago_end = today - DT.timedelta(days=days)
        szdays_ago_end = days_ago_end.strftime('%s')

        new_date = days_ago_end - DT.timedelta(minutes=window)
        days_ago_begin = today - DT.timedelta(days=days, minutes=window)
        szdays_ago_begin = days_ago_begin.strftime('%s')

        return [int(szdays_ago_begin)*1000, int(szdays_ago_end)*1000]

    
    def construct_threshold_message(self,json,schedule,threshold_limit):
        current_message = json['actions']['notify-slack']['slack']['message']['text']
        schedule = schedule['window_size']
        threshold_limit = str(threshold_limit)
        new_message = current_message % (schedule, threshold_limit)
        json['actions']['notify-slack']['slack']['message']['text'] = new_message
        return json
        
        
    def construct_insertion_time_gte_threshold_message(self,json,schedule):
        current_message = json['input']['search']['request']['body']['query']['range']['insertion_time']['gte']
        szschedule = str(schedule['window_size'])
        new_message = current_message % szschedule
        json['input']['search']['request']['body']['query']['range']['insertion_time']['gte'] = new_message
        return json    

    def construct_insertion_time_lte_threshold_message(self,json,schedule):
        current_message = json['input']['search']['request']['body']['query']['range']['insertion_time']['lte']
        schedule = str(schedule['window_size'])
        print "SWCHEDULE: " + schedule
        print current_message
        new_message = current_message % schedule
        json['input']['search']['request']['body']['query']['range']['insertion_time']['lte'] = new_message
        return json    
    

    def constuct_queryjson(self, time_code):
        """
            expects:
            [1514969690, 1514973290]
            returns:
            json

        """
        construct ="""
                {
                    "query" : {
                        "range" : {
                            "insertion_time" : {
                                "gte": "now-60m/m"
                            }
                        }
                    }
                }
        """        
        json_construct=json.loads(construct)
        szformat = '"format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"'
        query_payload = json.loads(' { ' + szformat + ', "gte": "' +  str(time_code[0]) + '", "lte": "' +  str(time_code[1]) + '"}')
        json_construct['query']['range']['insertion_time'] = query_payload
        return json_construct

