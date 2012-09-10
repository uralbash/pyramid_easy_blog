# -*- coding: utf8 -*-
#orignal file https://github.com/Studio-42/elfinder-python/blob/master/connector.py
#changed by Alexandr Rakov 08-03-2012

import json
import elFinder
from pyramid.response import Response
from cgi import FieldStorage

#connector opts
_opts = {
	#'root' and url rewrite from ini file
	'root': '/tmp',
	'URL': 'http://localhost:8080/static/uploaded',
	## other options
	'debug': True,
	'fileURL': True,  # if False: download files using connector, no direct urls to files
	# 'dirSize': True,
	# 'dotFiles': True,
	'fileMode': 0666,
	'dirMode': 0777,
	# 'uploadDeny': ['image', 'application'],
	# 'uploadAllow': ['image/png', 'image/jpeg'],
	# 'uploadOrder': ['deny', 'allow']
}

def connector(request):
    # init connector and pass options
    elf = elFinder.connector(_opts)

    # fetch only needed GET/POST parameters
    httpRequest = {}
    form=request.params
    for field in elf.httpAllowedParameters:
        if field in form:
            # Russian file names hack
            if field == 'name':
                httpRequest[field] = form.getone(field).encode('utf-8')

            elif field == 'targets[]':
                httpRequest[field] = form.getall(field)

            # handle CGI upload
            elif field == 'upload[]':
                upFiles = {}
                cgiUploadFiles = form.getall(field)
                for up in cgiUploadFiles:
                    if isinstance(up, FieldStorage):
                        upFiles[up.filename.encode('utf-8')] = up.file # pack dict(filename: filedescriptor)
                httpRequest[field] = upFiles
            else:
                httpRequest[field] = form.getone(field)

    # run connector with parameters
    status, header, response = elf.run(httpRequest)

    # get connector output and print it out

    result=Response(status=status)
    try:
        del header['Connection']
    except:
        pass
    result.headers=header

    if not response is None and status == 200:
        # send file
        if 'file' in response and isinstance(response['file'], file):
            result.body=response['file'].read()
            response['file'].close()

        # output json
        else:
            result.body=json.dumps(response)
    return result
    return """{"cwd":{"mime":"directory","ts":1345792824,"read":1,"write":1,"size":0,"hash":"l2_Lw","volumeid":"l2_","name":"Test here","locked":1,"dirs":1},"options":{"path":"Test here","url":"http:\/\/elfinder.org\/files\/test\/","tmbUrl":"http:\/\/elfinder.org\/files\/test\/.tmb\/","disabled":[],"separator":"\/","copyOverwrite":1,"archivers":{"create":["application\/x-tar","application\/x-gzip","application\/x-bzip2","application\/zip","application\/x-rar","application\/x-7z-compressed"],"extract":["application\/x-tar","application\/x-gzip","application\/x-bzip2","application\/zip","application\/x-rar","application\/x-7z-compressed"]}},"files":[{"mime":"directory","ts":1345792824,"read":1,"write":1,"size":0,"hash":"l2_Lw","volumeid":"l2_","name":"Test here","locked":1,"dirs":1},{"mime":"directory","ts":1334071677,"read":1,"write":0,"size":0,"hash":"l1_Lw","volumeid":"l1_","name":"Demo","locked":1,"dirs":1},{"mime":"directory","ts":1340114567,"read":0,"write":0,"size":0,"hash":"l1_QmFja3Vw","name":"Backup","phash":"l1_Lw","locked":1},{"mime":"directory","ts":1310252178,"read":1,"write":0,"size":0,"hash":"l1_SW1hZ2Vz","name":"Images","phash":"l1_Lw","locked":1},{"mime":"directory","ts":1310250758,"read":1,"write":0,"size":0,"hash":"l1_TUlNRS10eXBlcw","name":"MIME-types","phash":"l1_Lw","locked":1},{"mime":"directory","ts":1268269762,"read":1,"write":0,"size":0,"hash":"l1_V2VsY29tZQ","name":"Welcome","phash":"l1_Lw","locked":1,"dirs":1},{"mime":"directory","ts":1345792824,"read":1,"write":1,"size":0,"hash":"l2_Lw","volumeid":"l2_","name":"Test here","locked":1,"dirs":1},{"mime":"directory","ts":1345793414,"read":1,"write":1,"size":0,"hash":"l2_dGVzdGluZw","name":"testing","phash":"l2_Lw","dirs":1},{"mime":"image\/jpeg","ts":1345787801,"read":1,"write":1,"size":12617,"hash":"l2_MDcxZjEwNjJlMDJlYWJjOTVhMmE2NGVmYjVkNDQ0OGIuanBn","name":"071f1062e02eabc95a2a64efb5d4448b.jpg","phash":"l2_Lw","tmb":"l2_MDcxZjEwNjJlMDJlYWJjOTVhMmE2NGVmYjVkNDQ0OGIuanBn1345787801.png"},{"mime":"application\/x-tar","ts":1345789288,"read":1,"write":1,"size":20480,"hash":"l2_MDcxZjEwNjJlMDJlYWJjOTVhMmE2NGVmYjVkNDQ0OGIuanBnLnRhcg","name":"071f1062e02eabc95a2a64efb5d4448b.jpg.tar","phash":"l2_Lw"},{"mime":"image\/jpeg","ts":1345792824,"read":1,"write":1,"size":42888,"hash":"l2_NTU4MTczXzQ4NTE5NTgzMTQ5MDkyM18xMTQzMzY1MjQ2X24uanBn","name":"558173_485195831490923_1143365246_n.jpg","phash":"l2_Lw","tmb":"l2_NTU4MTczXzQ4NTE5NTgzMTQ5MDkyM18xMTQzMzY1MjQ2X24uanBn1345792824.png"},{"mime":"image\/jpeg","ts":1345783085,"read":1,"write":1,"size":94836,"hash":"l2_ODU4NjUwOV9aZDVlcyBjb3B5IDEuanBlZw","name":"8586509_Zd5es copy 1.jpeg","phash":"l2_Lw","tmb":"l2_ODU4NjUwOV9aZDVlcyBjb3B5IDEuanBlZw1345783085.png"},{"mime":"image\/jpeg","ts":1345785915,"read":1,"write":1,"size":2237097,"hash":"l2_Q29weSBvZiBEU0MwMTM0Ny5KUEc","name":"Copy of DSC01347.JPG","phash":"l2_Lw","tmb":"l2_Q29weSBvZiBEU0MwMTM0Ny5KUEc1345785915.png"},{"mime":"audio\/mpeg","ts":1345772686,"read":1,"write":1,"size":8801625,"hash":"l2_Um95IEpvbmVzIC0gQ2FuJ3QgYmUgdG91Y2hlZC5tcDM","name":"Roy Jones - Can't be touched.mp3","phash":"l2_Lw"},{"mime":"image\/jpeg","ts":1345784378,"read":1,"write":1,"size":20690,"hash":"l2_c21yMzYwMF8uanBn","name":"smr3600_.jpg","phash":"l2_Lw","tmb":"l2_c21yMzYwMF8uanBn1345784378.png"},{"mime":"text\/plain","ts":1345770710,"read":1,"write":1,"size":10,"hash":"l2_dGVzdC50eHQ","name":"test.txt","phash":"l2_Lw"},{"mime":"image\/jpeg","ts":1345788777,"read":1,"write":1,"size":105542,"hash":"l2_V2ludGVyLmpwZw","name":"Winter.jpg","phash":"l2_Lw","tmb":"l2_V2ludGVyLmpwZw1345788777.png"}],"api":"2.0","uplMaxSize":"16M","netDrivers":[],"debug":{"connector":"php","phpver":"5.3.14-1~dotdeb.0","time":0.096000194549561,"memory":"1333Kb \/ 1225Kb \/ 128M","upload":"","volumes":[{"id":"l1_","name":"localfilesystem","mimeDetect":"internal","imgLib":"imagick"},{"id":"l2_","name":"localfilesystem","mimeDetect":"internal","imgLib":"gd"}],"mountErrors":[]}}"""

def includeme(config):
    _opts['root']=config.registry.settings['elfinder_root']
    _opts['URL']=config.registry.settings['elfinder_url']

    config.add_route('connector', '/connector')
    config.add_view(connector,route_name='connector')
