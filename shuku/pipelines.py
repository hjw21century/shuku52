# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))

class ShukuPipeline(object):
    def process_item(self, item, spider):
    	#print("------------->" + item["title"][0:-3])
    	title=item["title"]
    	
    	with open('./' + title[0:title.find("【")] + '.txt', 'a+') as f:
    		for chunk in chunkstring(item["content"],32):
	    		f.write(chunk)
	    		f.write("\n")
	    	f.write("\n\n")
	    	f.close()
    	return item
