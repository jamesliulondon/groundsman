
import elasticsearch , urllib2 , base64, json

class Uri_tools():
    
    """
        def curl_metric(self, url, json_object, usr='elastic', pwd='changeme'):
            """ """
            print url
            request = urllib2.Request(url, json_object, {'Content-Type': 'application/json'})
            request.get_method = lambda: 'PUT'
            base64string = base64.b64encode('%s:%s' % (usr, pwd)).replace('\n', '')
            request.add_header("Authorization", "Basic %s" % base64string)   
            result = urllib2.urlopen(request)
            #print result
    """        

    def connect_elastic(self,elastic_host,e_user,e_pass,index,dtype,json_timerange):
        es = elasticsearch.Elasticsearch(elastic_host,
            http_auth=(e_user, e_pass)
            )
        result = es.count(index=index, doc_type=dtype, body=json_timerange)
        return result



    def arm_elastic_threshold(self,elastic_host,e_user,e_pass,watcher,body):
        url = 'http://' + elastic_host + ':9200/_xpack/watcher/watch/' + watcher
        print url
        print json.dumps(body)
        request = urllib2.Request(url, json.dumps(body), {'Content-Type': 'application/json'})
        request.get_method = lambda: 'PUT'
        base64string = base64.b64encode('%s:%s' % (e_user, e_pass)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)

        response = urllib2.urlopen(request)
        #return response.read()
        try:
            response = urllib2.urlopen(request)
            return response.read()
        except:
            print "ERROR POSTING"
            pass
            #print result

    def disarm_elastic_threshold(self,elastic_host,e_user,e_pass,watcher,body):
        url = 'http://' + elastic_host + ':9200/_xpack/watcher/watch/' + watcher
        print "http://" +elastic_host 
        request = urllib2.Request(url, json.dumps(body), {'Content-Type': 'application/json'})
        request.get_method = lambda: 'DELETE'
        base64string = base64.b64encode('%s:%s' % (e_user, e_pass)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)   
        try:
            response = urllib2.urlopen(request)
            return response.read()
        except:
            print "ERROR DELETING"
            pass
            #print result

        