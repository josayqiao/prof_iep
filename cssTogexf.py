# -*- coding: utf-8 -*-
import re


verbose=0
export_gexf=1
export_dot=1

if export_gexf :
	import gexf


def supprime_accent(ligne):
        """ supprime les accents du texte source """
        accents = { 'a': ['à', 'ã', 'á', 'â'],
                    'e': ['é', 'è', 'ê', 'ë'],
                    'i': ['î', 'ï'],
                    'u': ['ù', 'ü', 'û','Ü'],
                    'o': ['ô', 'ö','Ö'],
                    'c' : ['ç'] }
        for (char, accented_chars) in accents.iteritems():
            for accented_char in accented_chars:
                ligne = ligne.replace(accented_char, char)
        return ligne



def loadCategory(file):
# load a csv 
# colomun 0 : category name
# column 1	: group1 name
# column 2	: group2 name
# column 3	: ID
# column 4	: entity name
# returns dict [id]=["cat","group1","group2","name"]
	
	cat=""
	group1=group2=""
	nbline=1
	codes={}
	lines = file.readlines()
	for line in lines:
		try :
			data=line.split(";")
			#print str(nbline)+":"+data[0]
			if not data[0]=="" :
				cat=data[0]
			else : 
				group1=data[1] if not data[1]=="" else group1
				group2=data[2] if not data[2]=="" else group2
				id=data[3] if len(data)>=4 else ""
				if not id=="" :
					name=re.sub("[\r\n]","",data[4]) if len(data)>=5 else ""
					codes[id]=[supprime_accent(cat),supprime_accent(group1),supprime_accent(group2),supprime_accent(name),id]
		except Exception as e :
			print "error line "+str(nbline)+" : "+line
			print e
		nbline+=1

	return codes
	
def loadProf(file):
# load a csv 
# columns :
# NOM	DISCI	FORMATION1	F2	F3	DIPLOME1	D2	PRO1	T1	PRO2	T2	PRO3	T3	PRO4	T4	PRO5	T5	PRO6	T6	PRO7	T7	EXTRA1	T2	EXTRA2	T2	EXTRA3	T3	EXTRA4	T4	EXTRA5	T5	EXTRA6	T6
#
# this function will extract :  
# colomun 0 :  name
# column 2	: formation 
# column 3	: f2
# column 4	: f3
# column 7	: profession 
# column 9	: f2
# column 11	: f3
# column 13	: f3
# column 15	: f3
# column 17	: f3
# column 19	: f3
	
	
	profs=[]
	lines = file.readlines()
	nbline=1
	for line in lines:
		try :
			data=line.split(";")
			
			name=data[0]
			formations=[d for d in data[2:4] if not d in ("999","") ]
			professions=[d for i,d in enumerate(data[7:20]) if not d in ("999","") and i%2==0]
			if len(professions)>0 : #len(formations)>0 or 
				profs.append([supprime_accent(name),map(supprime_accent,formations),map(supprime_accent,professions),nbline])
			else :
				print " no formation or no profession"+name+str(len(formations))+" "+str(len(professions)) 
		except Exception as e:
			print " error line "+str(nbline)+" : "+line
			print e
		nbline+=1

	return profs	
	

def getDotLinkString(node1,node2,weight,label) :
	#return '"'+node1+'"->"'+node2+'",weight='+weight+',label="'+label+'";\n'
	return ''+node1+'->'+node2+'&sep;'+weight+'&sep;'+label+'\n'

def generateProfToProfGraph(profs,professionsCat,file_prefix):
	print "graph prof to prof"
	dotString=""
	idEdge=0
	
	if export_gexf :
		gexf_file=gexf.Gexf("Paul Girard medialab Sciences Po","IEP professers linked by common institutions "+file_prefix)
		graph=gexf_file.addGraph("undirected","static")
		
		for name,formations,professions,id in profs :
			graph.addNode(str(id),name)
		
		
	for prof1, prof2 in [(p1,p2) for i,p1 in enumerate(profs) for p2 in profs[i:] if p1!=p2] :
		# pour toutes les professions du prof 1
			# si la profession est présente dans celle du prof2
			if profID in prof2[2] :
				weight+=1
		if weight>0 :
			# on ajoute un lien
			if export_gexf  :
			if export_dot :
				dotString+=getDotLinkString(str(prof1[3])+"-"+prof1[0],str(prof2[3])+"-"+prof2[0],str(weight)," | ".join(labels))
			idEdge+=1
	
	if export_gexf  :
		file=open("profiep_profToprof_"+file_prefix+".gexf","w+")
		gexf_file.write(file)
	
	if export_dot :
		file=open("profiep_profToprof.dot","w+")
		file.write("digrpah output {\n"+dotString+"}")
		
		
################### INST TO INST #########################
#
#
##########################################################
def generateInstToInstGraph(profs,professionsCat,file_prefix):
	print "graph inst to inst"
	dotString=""
	idEdge=0
	
	if export_gexf :
		gexf_file=gexf.Gexf("Paul Girard medialab Sciences Po","Institutions linked by common IEP professers "+file_prefix)
		graph=gexf_file.addGraph("undirected","static")
		idAttInstCat2=graph.addNodeAttribute("cat2","","String")
		idAttInstCat1=graph.addNodeAttribute("cat1","","String")
		
		for cat,group1,group2,name,id in professionsCat.values() :
			n=graph.addNode(str(id),name if not name=="" else group2)
			n.addAttribute(idAttInstCat2,group2)
			n.addAttribute(idAttInstCat1,group1)
	
	
	for inst1,inst2 in [(inst1,inst2) for i,inst1 in enumerate(professionsCat.values()) for inst2 in professionsCat.values()[i:] if inst1!=inst2] :
		idinst1=inst1[4]
		idinst2=inst2[4]
		
		# pour toutes les professions du prof 1
		for prof in profs :
			# si inst1 et inst 2 sont présentes dans les professions du prof
				weight+=1
		if weight>0 :
			# on ajoute un lien
			node1=inst1[3] if not inst1[3]=="" else inst1[2]
			node2=inst2[3] if not inst2[3]=="" else inst2[2]

			if export_gexf :
			if export_dot :
				dotString+=getDotLinkString(node1,node2,str(weight)," | ".join(labels))
			idEdge+=1
				
	if export_gexf  :
		file=open("profiep_instToinst_"+file_prefix+".gexf","w+")
		gexf_file.write(file)
	
	if export_dot :
		file=open("profiep_instToinst.dot","w+")
		file.write("digrpah output {\n"+dotString+"}")

################### PROF TO INST #########################
#
#
##########################################################

def generateProfInstitutionGraph(profs,professionsCat,file_prefix):
	print "graph prof to inst"
	dotString=""
	idEdge=0
	

		
	if export_gexf :
		gexf_file=gexf.Gexf("Paul Girard medialab Sciences Po","Institutions and professers IEP "+file_prefix)
		graph=gexf_file.addGraph("undirected","static")
		idAttType=graph.addNodeAttribute("type","professer","String")
		idAttInstCat=graph.addNodeAttribute("cat2","","String")
		idAttInstCat1=graph.addNodeAttribute("cat1","","String")

		
		for cat,group1,group2,name,id in professionsCat.values() :
			n=graph.addNode("inst_"+str(id),name if not name=="" else group2)
			
			n.addAttribute(idAttType,"institution")
			
			n.addAttribute(idAttInstCat,group2)
			n.addAttribute(idAttInstCat1,group1)
			
		for name,formations,professions,id in profs :
			n=graph.addNode("prof_"+str(id),name)
			n.addAttribute(idAttType,"professer")
	
	for prof in profs :
		# pour toutes les professions du prof 1
			if export_gexf :
				idEdge+=1	
			if export_dot :
				profession=professionsCat[instID][3] if not professionsCat[instID][3]=="" else professionsCat[instID][2]
				dotString+=getDotLinkString(str(prof[3])+"-"+prof[0],profession,"1","")	
	if export_gexf :
		file=open("profiep_profToinst_"+file_prefix+".gexf","w+")
		gexf_file.write(file)
	
	if export_dot :
		file=open("profiep_profToinst.dot","w+")
		file.write("digrpah output {\n"+dotString+"}")	
			
# load categories

# profession
file=open("profession.csv")
professionsCat=loadCategory(file)
#print professions
if verbose :
	for id,vals in professionsCat.iteritems() :
		print id+"|"+"|".join(vals)

# formation

# extra



for year in ("1970","2008") :
	# load prof
	file=open(year+".csv")
	profs=loadProf(file)
	print year+": number profs loaded :"+str(len(profs))
	#print professions
	if verbose :
		for name,formations,professions,id in profs :
			print name+"|"+"|".join([professionsCat[p][3] if not professionsCat[p][3]=="" else professionsCat[p][2] for p in professions])
	# let's gexf this
	
	# node = professers
	# links = shared institutions
	# nodes
	key=lambda prof:prof[0]
	profs=sorted(profs, key=key )
	
	
	generateProfInstitutionGraph(profs,professionsCat,year)
	generateProfToProfGraph(profs,professionsCat,year)
	generateInstToInstGraph(profs,professionsCat,year)









