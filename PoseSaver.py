#The Tool is Used for Saving Pose in Maya
#Author: Ryan
#Email: tenghaow@andrew.cmu.edu

from xml.dom.minidom import Document
from xml.dom.minidom import parse
from xml.dom.minidom import parseString
'''use etree to read the xml_file'''
import xml.etree.ElementTree as ET
import maya.cmds as maya
from functools import partial

''' for each pose save all the attribute property'''
'''for saving all the data'''
Data_dic = dict()
windowID = 'guiwindow'
textfieldID = 'Dataname'
layoutID = 'coluumnlayout'
tabID='mytablayout'
formlayout_flag = False
shelf_dic = dict()
perspcam=''

class Hierachy_Data(object):

    """docstring for Hierachy_Data"""

    def __init__(self, name):
        super(Hierachy_Data, self).__init__()
        self.name = name
        self.keylist = [] #new keylist for each Data
        self.pose_dict = dict() #new pose_dict for each Data

###used for build the UI for Pose Saver
# save the data to array
def ui_block(Data_name):
    global formlayout_flag
    #print formlayout_flag
    if(not formlayout_flag):
        #print "create formLayout"
        maya.setParent(layoutID)
        #global formlayout_flag
        formlayout_flag = True
        myform = maya.formLayout()
        mytab = maya.tabLayout(tabID)
        maya.formLayout(myform, e=True, af=[
                        (mytab, 'top', 10), (mytab, 'bottom', 10), (mytab, 'left', 7), (mytab, 'right', 10)])
    childarray=maya.tabLayout(tabID,q=True,ca=True)
    if childarray == None:
        childarray=[]
    if Data_name in childarray:
        maya.warning('Data name exists')
        return
    mytabcolumn = maya.columnLayout(Data_name, w=360, h=500,p=tabID)
    shelf_dic[Data_name] = mytabcolumn
    maya.columnLayout(w=360,h=130,cat=('both',30),rs=5)
    maya.text(l='Object List:',al='left',fn='boldLabelFont',w=360,h=20)
    maya.textScrollList(Data_name+'_controller_list',w=300,h=100,ams=True,sc=select_obj)
    maya.setParent('..')

    maya.rowColumnLayout(
        w=360, h=70, nc=2, cs=[(1, 30), (2, 100), (3, 30)],rs=(1,5))
    AddObject = maya.button(
        l='Add Object', w=100, h=25, al='center',c=addobject)
    DelObject = maya.button(
        l='Delete Object', w=100, h=25, al='center',c=delobject)

    ExportList = maya.button(
        l='Export List', w=100, h=25, al='center')
    ImportList = maya.button(
        l='Import List', w=100, h=25, al='center')

    maya.setParent('..')
    seprator1 = maya.separator(w=400, h=10)
    maya.columnLayout(w=360,h=50,cat=('both',30),rs=5)
    maya.text(l='Pose Name:',al='left',w=400,fn='boldLabelFont')
    textfield1 = maya.textField(
        Data_name+'posename',  pht='put the pose name here...', w=300, h=20)#, bc=partial(save_pose, Data_name)
    maya.setParent('..')
    maya.rowColumnLayout(
        w=360, h=40, nc=2, cs=[(1, 30), (2, 100), (3, 30)],rs=(1,5))
    addpose = maya.button(
        l='Add Pose', w=100, h=25, al='center',c=add_pose)
    # exportbutton=maya.button(l='Export',w=100,h=20,al='center',c=partial(export_hierachy))
    renamepose = maya.button(
        l='Rename Pose', w=100, h=25, al='center',c=rename_pose)
    maya.setParent('..')
    maya.columnLayout(w=360, h=130, cat=('left', 30),rs=5)
    maya.text(l='Pose List:',al='left',w=400,fn='boldLabelFont')
    maya.textScrollList(Data_name+'_poselist',w=300,h=100,sc=read_data)
    maya.setParent('..')
    maya.rowColumnLayout(
        w=360, h=80, nc=2, cs=[(1, 30), (2, 100), (3, 30)],rs=(1,5))
    maya.button(l='Keyframe Pose', w=100, h=25, al='center',c=keyframe_pose)
    maya.button(l='Remove Pose', w=100, h=25, al='center',c=delete_pose)
    maya.button(l='Export Pose', w=100, h=25, al='center',c=export_pose)
    maya.button(l='Import Pose', w=100, h=25, al='center',c=import_pose)
#

def ui_initializer():
    if len(Data_dic.keys())==0:
        return
    for Dataname in Data_dic.keys():
        ui_block(Dataname)
        temp_data=Data_dic[Dataname]
        keylist=temp_data.keylist
        print temp_data.pose_dict.keys()
        maya.textScrollList(Dataname+'_controller_list',e=True,a=keylist)
        for posename in temp_data.pose_dict.keys():
            #print '123'
            maya.textScrollList(Dataname+'_poselist',e=True,a=posename)

def select_obj(*arg):
    Data_name=maya.tabLayout(tabID,q=True,st=True)
    controller=maya.textScrollList(Data_name+'_controller_list',q=True,si=True)
    maya.select(controller)

# save the data to array
def constructdata(* arg):
    Data_name = maya.textField(textfieldID, q=True, tx=True)
    ui_block(Data_name)
    Data_dic[Data_name]=Hierachy_Data(Data_name)
    updateXML_data()

def removedata(*arg):
    #return current dataname
    index=maya.tabLayout(tabID,q=True,sti=True)
    print index
    Tablist=maya.tabLayout(tabID,q=True,tli=True)
    print Tablist[index-1]
    Dataname=Tablist[index-1]
    maya.deleteUI(shelf_dic[Dataname])
    del shelf_dic[Dataname]
    del Data_dic[Dataname]
    if (len(shelf_dic.keys())==0):
        maya.deleteUI(tabID)
        global formlayout_flag
        formlayout_flag=False
    updateXML_data()

def renamedata(*arg):
    newname= maya.textField(textfieldID, q=True, tx=True)
    index=maya.tabLayout(tabID,q=True,sti=True)
    Tablist=maya.tabLayout(tabID,q=True,tli=True)
    print Tablist
    Dataname=Tablist[index-1]
    maya.tabLayout(tabID,e=True,tl=[shelf_dic[Dataname],newname])
    shelf_dic[newname]=shelf_dic[Dataname]
    Data_dic[newname]=Data_dic[Dataname]
    del Data_dic[Dataname]
    del shelf_dic[Dataname]
    updateXML_data()

#create customchannel for save the posedata
def add_attribute():
    xml_init='<?xml version="1.0" ?><data></data>'
    #find the perspective camera
    if maya.objExists('persp'):
        global perspcam
        perspcam=maya.ls('persp')[0]
        if not maya.attributeQuery('posedata_xml',node='persp',ex=True):
            maya.addAttr(perspcam,ln='posedata_xml',dt='string')
            maya.setAttr(perspcam +'.posedata_xml',xml_init,type='string')

def addobject(*arg):
    Dataname=maya.tabLayout(tabID,q=True,st=True)
    temp_data=Data_dic[Dataname]
    print Dataname
    posecontroller = maya.ls(sl=True,typ='transform')
    existcontroller=maya.textScrollList(Dataname+'_controller_list',q=True,ai=True)
    if existcontroller == None:
        existcontroller=[]
    addobj=[]
    for controller in posecontroller:
        if controller not in existcontroller:
            addobj.append(controller)
    maya.textScrollList(Dataname+'_controller_list',e=True,a=addobj)
    temp_data.keylist=maya.textScrollList(Dataname+'_controller_list',q=True,ai=True)
    updateXML_data()

def delobject(*arg):
    Dataname=maya.tabLayout(tabID,q=True,st=True)
    temp_data=Data_dic[Dataname]
    selobj=maya.textScrollList(Dataname+'_controller_list',q=True,si=True)
    if not selobj==None:
        maya.textScrollList(Dataname+'_controller_list',e=True,ri=selobj)
        temp_data.keylist=maya.textScrollList(Dataname+'_controller_list',q=True,ai=True)
    updateXML_data()

#getsettableChannls
    #  BUG some Compound attrs such as constraints return invalid data for some of the
    #  base functions using this as they can't be simply set. HardCode here to strip them out
    #  ie: pointConstraint.target.targetWeight
    #  ie: pointConstraint.vector returns compound attrs
def getChannelBoxAttrs(controller):
    filtred_controllerAttr=[]
    controllerAttr = maya.listAttr(
            controller, r=True, v=True, k=True, u=True)
    for attr in controllerAttr:
        attrtype=maya.getAttr(controller+'.'+attr)
        if '.' not in str(attr) and not isinstance (attrtype,list):
            filtred_controllerAttr.append(attr)
    return filtred_controllerAttr


# save the data
def add_pose(*arg):
    Data_name=maya.tabLayout(tabID,q=True,st=True)
    temp_data=Data_dic[Data_name]
    print Data_name+'controller_list'
    temp_data.keylist = maya.textScrollList(Data_name+'_controller_list',q=True,ai=True)
    print temp_data.keylist
    if temp_data.keylist == None:
        return
    Pose_name =  maya.textField(Data_name+'posename', q=True, tx=True)
    #data_class = Data_dic[Data_name]
    # print data_class.name
    # print data_class.pose_dict
    if not Pose_name:
        maya.warning('please give the pose a name')
        return
    if searchpose(Pose_name, temp_data.pose_dict):
        maya.warning('please rename the pose!')
        return
    # pose_dic=dict()
    posecontroller =temp_data.keylist
    print posecontroller
    controllerdic = dict()
    for controller in posecontroller:
        controllerAttr = getChannelBoxAttrs(controller)#maya.listAttr(
            #controller, r=True, v=True, k=True, u=True, c=True)
        AttrList = []
        print controllerAttr
        for Attr in controllerAttr:
            print Attr
            AttrList.append(maya.getAttr(controller+'.'+Attr))
        controllerdic[controller] = AttrList
    '''save the controller list and pose name'''
    temp_data.pose_dict[Pose_name] = controllerdic
    '''save the data to the pose list'''
    maya.textScrollList(Data_name+'_poselist',e=True,a=Pose_name)
    #Data_dic[Data_name]=temp_data
    #save xml when add new pose
    updateXML_data()



def searchpose(posename, pose_dict):
    pose_exsit = False
    if posename in pose_dict:
        print 'find the pose'
        return True
    return False

def rename_pose(*arg):
    Data_name=maya.tabLayout(tabID,q=True,st=True)
    temp_data=Data_dic[Data_name]
    posename=maya.textScrollList(Data_name+'_poselist',q=True,si=True)
    if posename==None:
        return
    new_posename= maya.textField(Data_name+'posename', q=True, tx=True)
    if new_posename==None:
        return
    if searchpose(new_posename, temp_data.pose_dict):
        maya.warning('new name exist')
        return
    temp_data.pose_dict[new_posename[0]]=temp_data.pose_dict[posename[0]]
    del temp_data.pose_dict[posename[0]]
    maya.textScrollList(Data_name+'_poselist',e=True,ri=posename)
    maya.textScrollList(Data_name+'_poselist',e=True,a=new_posename)
    #temp_data.pose_dict[]
    #Data_dic[Data_name]=temp_data
    print temp_data.pose_dict
    #print Data_dic[Data_name].pose_dict
    updateXML_data()

# read the data
def read_data(*arg):
    Data_name=maya.tabLayout(tabID,q=True,st=True)
    temp_data = Data_dic[Data_name]
    posename=maya.textScrollList(Data_name+'_poselist',q=True,si=True)
    #print temp_data.name
    #print temp_data.pose_dict[posename[0]]
    pose = searchpose(posename[0], temp_data.pose_dict)
    if(pose):
        print temp_data.keylist
        for controller in temp_data.keylist:
            controllerAttr = getChannelBoxAttrs(controller)#maya.listAttr(
                #controller, r=True, v=True, k=True, c=True)
            #print controllerAttr
            i = 0
            for Attr in controllerAttr:
                if type(temp_data.pose_dict[posename[0]][controller][i]) == type(str()):
                    s = temp_data.pose_dict[posename[0]][controller][i]
                    temp_data.pose_dict[posename[0]][controller][i]=data_process(s)
                    #print type(s)
                    #print type(temp_data.pose_dict[posename[0]][controller][i])
                print controller+'.'+Attr
                print temp_data.pose_dict[posename[0]][controller][i]
                maya.setAttr(
                    controller+'.'+Attr, temp_data.pose_dict[posename[0]][controller][i])
                i = i+1
    else:
        print 'cannot find the pose'

#process data 
def data_process(str):
	str_temp=str
	#test the data is float or not, remove the '.' inside the number
	if '.' in str:
		str_temp=str.replace('.','')
	#if data is less than zero, remove the '-' at the start of the number
	if str.startswith('-'):
		str_temp=str_temp.replace('-','')
	#if the processed data is all digit convert the string to float
	if str_temp.isdigit():
		str=float(str)
		return str
	#if the attr is all alphabetic /true of flase convert the string to boolean
	if str.isalpha():
		str=bool(str)
		return str



def keyframe_pose(*arg):
    Data_name=maya.tabLayout(tabID,q=True,st=True)
    temp_data = Data_dic[Data_name]
    posename=maya.textScrollList(Data_name+'_poselist',q=True,si=True)
    if posename==None:
        return
    pose = searchpose(posename[0], temp_data.pose_dict)
    if(pose):
        # i=1
        for controller in temp_data.keylist:
            controllerAttr = getChannelBoxAttrs(controller)#maya.listAttr(
                #controller, r=True, v=True, k=True, c=True)
            i = 0
            for Attr in controllerAttr:
                # print controller
                # print Attr
                maya.setAttr(
                    controller+'.'+Attr, temp_data.pose_dict[posename[0]][controller][i])
                maya.setKeyframe(controller, at=Attr)
                i = i+1


def delete_pose(*arg):
    Data_name=maya.tabLayout(tabID,q=True,st=True)
    temp_data = Data_dic[Data_name]
    posename=maya.textScrollList(Data_name+'_poselist',q=True,si=True)
    if posename==None:
        return
    print temp_data.pose_dict[posename[0]]
    pose = searchpose(posename[0], temp_data.pose_dict)
    if(pose):
        del temp_data.pose_dict[posename[0]]
        maya.textScrollList(Data_name+'_poselist',e=True,ri=posename)
    updateXML_data()

def export_pose(*arg):
    Data_name=maya.tabLayout(tabID,q=True,st=True)
    temp_data = Data_dic[Data_name]
    posename=maya.textScrollList(Data_name+'_poselist',q=True,si=True)
    if posename==None:
        return
    posedic = temp_data.pose_dict[posename[0]]
    scenename = maya.file(sn=True, q=True)
    doc = Document()
    #print scenename
   # print posedic
    #print posename[0]
    #root_node=doc.createElement('Posename: '+Pose_name+ '(filename: {0})'.format(scenename))
    root_node = doc.createElement('PoseData')
    doc.appendChild(root_node)
    file_node = doc.createElement('Filename')
    root_node.appendChild(file_node)
    file_node.setAttribute('FilePath', str(scenename))
    pose_node = doc.createElement('Posename')
    file_node.appendChild(pose_node)
    pose_node.setAttribute('PoseName', str(posename[0]))
    # print pose_controller
    for controller in temp_data.keylist:
        controller_node = doc.createElement('Controller')
        pose_node.appendChild(controller_node)
        controller_node.setAttribute('Controller', str(controller))
        controllerAttr = getChannelBoxAttrs(controller)#maya.listAttr(
            #controller, r=True, v=True, k=True, c=True)
        i = 0
        for atrributes in controllerAttr:
            attr_node = doc.createElement('Attributes')
            controller_node.appendChild(attr_node)
            attr_node.setAttribute(atrributes, str(posedic[controller][i]))
            i = i+1
    # print pose_attributes
    # xml_file_path=maya.workspace(q=True,dir=True)
    xml_file_path = maya.fileDialog2(ff='*.xml')
    print xml_file_path
    if not xml_file_path == None:
        print xml_file_path
        xml_file = open(xml_file_path[0], 'w')
        xml_file.write(doc.toprettyxml())
        xml_file.close()
        print doc.toprettyxml()
    # print posedata

def import_pose(*arg):
    Data_name=maya.tabLayout(tabID,q=True,st=True)
    temp_data = Data_dic[Data_name]
    # pose=dict()
    print temp_data.keylist
    xml_file_path = maya.fileDialog(dm='*.xml')
    print xml_file_path
    dom = parse(xml_file_path)
    for node in dom.getElementsByTagName('Posename'):
        controller = dict()
        namekey = node.attributes.keys()
        print namekey[0]
        posepair = node.attributes[namekey[0]]
        print posepair.value
        for node in dom.getElementsByTagName('Controller'):
            attrlist = []
            controllerkey = node.attributes.keys()
            print controllerkey[0]
            controllerpair = node.attributes[controllerkey[0]]
            for nnode in node.getElementsByTagName('Attributes'):
                attrs = nnode.attributes.keys()
                # print attrs[0]
                pair = nnode.attributes[attrs[0]]
                #print (str(pair.name)+'='+str(pair.value))
                print pair.value
                attrlist.append(str(pair.value))
            print controllerpair.value
            print attrlist
            controller[controllerpair.value] = attrlist
        temp_data.pose_dict[posepair.value] = controller
        maya.textScrollList(Data_name+'_poselist',e=True,a=posepair.value)
    print temp_data.pose_dict
    updateXML_data()

def updateXML_data():
    doc = Document()
    root_node=doc.createElement('data')
    doc.appendChild(root_node)
    for Data_name in Data_dic.keys():
        #print Data_name
        data_node=doc.createElement('Pose_Data')
        root_node.appendChild(data_node)
        data_node.setAttribute('Dataname', str(Data_name))
        temp_data = Data_dic[Data_name]
        #print temp_data
        print Data_name
        print Data_dic[Data_name].pose_dict
        for posename in temp_data.pose_dict.keys():
            posedic = temp_data.pose_dict[posename]
            #print posedic
            #print posename
            #root_node=doc.createElement('Posename: '+Pose_name+ '(filename: {0})'.format(scenename))
            pose_node = doc.createElement('Posename')
            data_node.appendChild(pose_node)
            pose_node.setAttribute('PoseName', str(posename))
            # print pose_controller
            for controller in temp_data.keylist:
                controller_node = doc.createElement('Controller')
                pose_node.appendChild(controller_node)
                controller_node.setAttribute('Controller', str(controller))
                controllerAttr = getChannelBoxAttrs(controller)#maya.listAttr(
                    #controller, r=True, v=True, k=True, c=True)
                i = 0
                for atrributes in controllerAttr:
                    attr_node = doc.createElement('Attributes')
                    controller_node.appendChild(attr_node)
                    attr_node.setAttribute(atrributes, str(posedic[controller][i]))
                    i = i+1
    print doc.toprettyxml()
    global perspcam
    maya.setAttr(perspcam +'.posedata_xml',doc.toprettyxml(),type='string')
    # print posedata

def LoadData_FromXML():
    global perspcam
    global Data_dic
    xml_string=str(maya.getAttr(perspcam+'.posedata_xml'))
    print xml_string
    #construct data_dic
    dom=parseString(xml_string)
    for data_node in dom.getElementsByTagName('Pose_Data'):
        data_key = data_node.attributes.keys()
        #print namekey[0]
        Data_name = data_node.attributes[data_key[0]].value
        #print Data_name
        temp_data=Hierachy_Data(Data_name)
        for posename_node in data_node.getElementsByTagName('Posename'):
            controller = dict()
            posename_key=posename_node.attributes.keys()
            pose_name=posename_node.attributes[posename_key[0]].value
            controllerlist=[]
            for controller_node in posename_node.getElementsByTagName('Controller'):
                attrlist = []
                controller_key = controller_node.attributes.keys()
                #print controller_key[0]
                controller_name = controller_node.attributes[controller_key[0]].value
                controllerlist.append(controller_name)
                #print controllerlist
                for attr_node in controller_node.getElementsByTagName('Attributes'):
                    attrs_key = attr_node.attributes.keys()
                    #print attrs_key[0]
                    attrs_value = attr_node.attributes[attrs_key[0]].value
                    #print attrs_value.value
                    attrlist.append(str(attrs_value))
                #print attrlist
                controller[controller_name] = attrlist
            temp_data.pose_dict[pose_name] = controller
            temp_data.keylist=controllerlist
        Data_dic[Data_name]=temp_data
        print Data_dic[Data_name].pose_dict
        print Data_dic[Data_name].keylist
 

def posesaver_pannel():
    maya.window(windowID, widthHeight=(
        400, 500), title='Pose Saver',s=True)
    form0=maya.formLayout('windowsform',p=windowID)
    layout = maya.columnLayout(layoutID,w=380)
    maya.formLayout(form0,e=True,af=[(layout,'top',10),(layout,'left',10),(layout,'right',10)])
    maya.text(l='Pose Saver Tool',
              al='center', w=380, h=20, fn='boldLabelFont', p=layout)
    maya.separator(p=layout,w=380,h=10)
    maya.columnLayout(w=380,h=50,cat=('both',20))
    maya.text(l='Data Name:',
              al='left', w=380, h=20, fn='boldLabelFont')
    maya.textField(textfieldID,pht='put the name here...', w=340,h=20)
    maya.setParent('..')
    maya.rowColumnLayout(
        w=380, h=35, nc=3, cs=[(1, 20), (2, 20),(3,20), (4, 20)],rs=(1,5))
    maya.button(l='Add Data', w=100, h=30, al='center',c=constructdata)
    maya.button (l='Remove Data',w=100,h=30,al='center',c=removedata)
    maya.button(l='Rename Data', w=100, h=30, al='center',c=renamedata)
    add_attribute()
    LoadData_FromXML()
    ui_initializer()
    #maya.showWindow(windowID)
    allowedAreas=['right','left']
    maya.dockControl('PoseSaver',a='right',con=windowID,aa=allowedAreas)



def rigginggui():
    if (maya.window(windowID, ex=True)):
        maya.deleteUI(windowID, wnd=True)
    if (maya.dockControl('PoseSaver',ex=True)):
        maya.deleteUI('PoseSaver')
    posesaver_pannel()


rigginggui()
