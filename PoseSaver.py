from xml.dom.minidom import Document
from xml.dom.minidom import parse
'''use etree to read the xml_file'''
import xml.etree.ElementTree as ET
import maya.cmds as maya
from functools import partial

''' for each pose save all the attribute property'''
'''for saving all the data'''
Data_dic = dict()
'''for saving individule data type'''
posedata_dic = dict()
windowID = 'guiwindow'
textfieldID = 'Enterhierachy'
textfieldID1 = 'posename'
layoutID = 'coluumnlayout'
tabID='mytablayout'
obj_list='objscrolllist'
# Pose_Button_Manger=[]
formlayout_flag = False
shelf_dic = dict()


class Hierachy_Data(object):

    """docstring for Hierachy_Data"""

    def __init__(self, name):
        super(Hierachy_Data, self).__init__()
        self.name = name
    keylist = []
    pose_dict = dict()
    pose_gui_dict = dict()


# save the data to array
def constructdata(* arg):
    Data_name = maya.textField(textfieldID, q=True, tx=True)
    posecontroller = maya.ls(sl=True)
    if not Data_name:
        maya.warning('Please give data a name...')
        return
    if not posecontroller:
        maya.warning('Please select at least one object...')
        return
    if Data_name in Data_dic:
        maya.warning('Data name exists!')
        return
    temp_data = Hierachy_Data(Data_name)
    temp_data.keylist = posecontroller
    #update objscroll
    #cmds.textScrollList(obj_list,e=True,a=posecontroller)
    Data_dic[Data_name] = temp_data
    print Data_dic[Data_name].keylist
    # print posedata_dic
    global formlayout_flag
    print formlayout_flag
    if(not formlayout_flag):
        print "create formLayout"
        maya.setParent(layoutID)
        #global formlayout_flag
        formlayout_flag = True
        myform = maya.formLayout()
        mytab = maya.tabLayout(tabID)
        maya.formLayout(myform, e=True, af=[
                        (mytab, 'top', 10), (mytab, 'bottom', 10), (mytab, 'left', 7), (mytab, 'right', 10)])
    mytabcolumn = maya.columnLayout(Data_name, w=460, h=550,p=tabID)
    shelf_dic[Data_name] = mytabcolumn
    #form1=maya.formLayout(p=myshelf,w=480,h=500)
    maya.columnLayout(w=460,h=130,p=mytabcolumn,cat=['both',50],rs=5)
    #maya.formLayout(form1,e=True,af=[(mylayout1,'top',10),(mylayout1,'right',10),(mylayout1,'left',10)])
    mytext=maya.text(l='Object List:',al='left',fn='boldLabelFont',w=430,h=20)
   # print mytext
    maya.textScrollList(obj_list,w=360,h=100)
    maya.setParent('..')

    maya.rowColumnLayout(
        w=460, h=80, nc=2, cs=[(1, 50), (2, 110), (3, 50)],rs=(1,5))
    deletebutton = maya.button(
        l='Add Object', w=125, h=30, al='center')
    importbutton = maya.button(
        l='Delete Object', w=125, h=30, al='center')

    deletebutton1 = maya.button(
        l='Export List', w=125, h=30, al='center')
    importbutton1 = maya.button(
        l='Import List', w=125, h=30, al='center')

    maya.setParent('..')
    seprator1 = maya.separator(w=500, h=20)
    maya.columnLayout(w=460,h=50,cat=('both',50),rs=5)
    maya.text(l='Pose Name:',al='left',w=400,fn='boldLabelFont')
    textfield1 = maya.textField(
        textfieldID1,  pht='put the pose name here...', w=360, h=20)#, bc=partial(save_pose, Data_name)
    maya.setParent('..')
    maya.rowColumnLayout(
        w=460, h=40, nc=2, cs=[(1, 50), (2, 110), (3, 50)],rs=(1,5))
    deletebutton = maya.button(
        l='Add Pose', w=125, h=30, al='center')
    # exportbutton=maya.button(l='Export',w=100,h=20,al='center',c=partial(export_hierachy))
    importbutton = maya.button(
        l='Rename Pose', w=125, h=30, al='center')
    maya.setParent('..')
    maya.columnLayout(w=460, h=130, cat=('left', 50),rs=5)
    maya.text(l='Pose List:',al='left',w=400,fn='boldLabelFont')
    maya.textScrollList(obj_list,w=360,h=100)
    maya.setParent('..')
    maya.rowColumnLayout(
        w=460, h=80, nc=2, cs=[(1, 50), (2, 110), (3, 50)],rs=(1,5))
    maya.button(l='Keyframe Pose', w=125, h=30, al='center')
    maya.button(l='Remove Pose', w=125, h=30, al='center')
    maya.button(l='Export Pose', w=125, h=30, al='center')
    maya.button(l='Import Pose', w=125, h=30, al='center')



def Remove_hierachy(*arg):
    print 'delete data'


def Import_hierachy(Data_name, *arg):
    data_class = Data_dic[Data_name]
    controller = dict()
    # pose=dict()
    print data_class.keylist
    xml_file_path = maya.fileDialog(dm='*.xml')
    print xml_file_path
    dom = parse("/Users/zifeiwang/Desktop/1.xml")
    for node in dom.getElementsByTagName('Posename'):
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
        data_class.pose_dict[posepair.value] = controller
        UIblock_creation(Data_name, posepair.value)
    print data_class.pose_dict


def validation_detection():
    '''detect current controller objects'''
    # print posedata[0]


def UIblock_creation(Data_name, Pose_name):
    data_class = Data_dic[Data_name]
    maya.setParent(shelf_dic[Data_name])
    #global Pose_button
    temp_layout1 = maya.columnLayout(w=400, h=80, cat=('left', 130))
    Pose_button = maya.button(l=Pose_name, al='center', w=200, h=50, c=partial(
        read_data, Data_name, Pose_name))
    print Pose_button
    maya.setParent('..')
    temp_layout2 = maya.rowColumnLayout(
        w=500, h=50, nc=3, cs=[(1, 25), (2, 30), (3, 30), (4, 30)])
    #global Del_Button
    #global Key_Button
    Key_Button = maya.button(
        l='Set Keyframe', w=120, h=35, c=partial(key_Frame, Data_name, Pose_name))
    Export_Button = maya.button(
        l='Export pose', w=120, h=35, c=partial(Export_pose, Data_name, Pose_name))
    Del_Button = maya.button(
        l='Delete', w=120, h=35, c=partial(delete_data, Data_name, Pose_name))
    maya.setParent('..')
    sep_block = maya.separator(w=500, h=10)
    # print Pose_button, Del_Button, Key_Button
    Buttongroup = (
        Pose_button, Del_Button, Key_Button, temp_layout1, temp_layout2, sep_block)
    data_class.pose_gui_dict[Pose_name] = Buttongroup
    print data_class.pose_gui_dict

# save the data


def save_pose(Data_name, *arg):
    Pose_name = maya.textFieldButtonGrp(textfieldID1, q=True, tx=True)
    data_class = Data_dic[Data_name]
    # print data_class.name
    # print data_class.pose_dict
    if not Pose_name:
        maya.warning('please give the pose a name')
        return
    if searchpose(Pose_name, data_class.pose_dict):
        maya.warning('please rename the pose!')
        return
    # pose_dic=dict()
    posecontroller = data_class.keylist
    print posecontroller
    controllerdic = dict()
    for controller in posecontroller:
        controllerAttr = maya.listAttr(
            controller, r=True, v=True, k=True, u=True, c=True)
        AttrList = []
        for Attr in controllerAttr:
            AttrList.append(maya.getAttr(controller+'.'+Attr))
        controllerdic[controller] = AttrList
    data_class.pose_dict[Pose_name] = controllerdic
    # print data_class.pose_dict
    '''save the controller list and pose name'''
    UIblock_creation(Data_name, Pose_name)
    print data_class.pose_dict
    # Pose_Button_Manger.append(Buttongroup)
    # print DataDic
    # print objecthierachy


def searchpose(posename, pose_dict):
    pose_exsit = False
    if posename in pose_dict:
        print 'find the pose'
        return True
    return False

# read the data
def read_data(Data_name, Pose_name, *arg):
    data_class = Data_dic[Data_name]
    print data_class.name
    print data_class.pose_dict[Pose_name]
    pose = searchpose(Pose_name, data_class.pose_dict)
    if(pose):
        print data_class.keylist
        for controller in data_class.keylist:
            controllerAttr = maya.listAttr(
                controller, r=True, v=True, k=True, c=True)
            print controllerAttr
            # print controllerAttr
            i = 0
            for Attr in controllerAttr:
                # print data_class.pose_dict[Pose_name][controller]
                #print (controller+'.'+Attr+'='+unicode(data_class.pose_dict[Pose_name][controller][i]))
                #print (type(unicode(data_class.pose_dict[Pose_name][controller][i])))
                # test input is str ot not
                # determine the data type is string or unicode
                if type(data_class.pose_dict[Pose_name][controller][i]) == type(str()):
                    s = data_class.pose_dict[Pose_name][controller][i]
                    data_class.pose_dict[Pose_name][controller][i]=data_process(s)
                    print type(s)
                    print type(data_class.pose_dict[Pose_name][controller][i])
                    #data_class.pose_dict[Pose_name][controller][i]=s
                    #print type(data_class.pose_dict[Pose_name][controller][i])

                    '''
                    print 'finish'
                    s_new=''
                    print s
                    if '.' in s:
                        s_new=s.replace('.', '')
                        print s_new
                    if s.startswith('-'):
                    	s_new=s_new.replace('-','')
                    	print s_new
                    if s_new.isdigit():
                         data_class.pose_dict[Pose_name][controller][i] = float(
                         data_class.pose_dict[Pose_name][controller][i])
                         print 'it is number'
                    if s.isalpha():
                         print 'it is bool'
                         data_class.pose_dict[Pose_name][controller][i] = bool(
                         data_class.pose_dict[Pose_name][controller][i])
					'''
                maya.setAttr(
                    controller+'.'+Attr, data_class.pose_dict[Pose_name][controller][i])
                i = i+1
    else:
        print 'cannot find the pose'

def data_process(str):
	str_temp=''
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






def delete_data(Data_name, Pose_name, *arg):
    data_class = Data_dic[Data_name]
    print data_class.pose_dict[Pose_name]
    pose = searchpose(Pose_name, data_class.pose_dict)
    if(pose):
        del data_class.pose_dict[Pose_name]
        for obj in data_class.pose_gui_dict[Pose_name]:
            cmds.deleteUI(obj)
        del data_class.pose_gui_dict[Pose_name]
    # print data_class.pose_dict
    # print data_class.pose_gui_dict


def key_Frame(Data_name, Pose_name, *arg):
    data_class = Data_dic[Data_name]
    pose = searchpose(Pose_name, data_class.pose_dict)
    if(pose):
        # i=1
        for controller in data_class.keylist:
            controllerAttr = maya.listAttr(
                controller, r=True, v=True, k=True, c=True)
            i = 0
            for Attr in controllerAttr:
                # print controller
                # print Attr
                maya.setAttr(
                    controller+'.'+Attr, data_class.pose_dict[Pose_name][controller][i])
                maya.setKeyframe(controller, at=Attr)
                i = i+1


def Export_pose(Data_name, Pose_name, *arg):
    data_class = Data_dic[Data_name]
    posedic = data_class.pose_dict[Pose_name]
    scenename = maya.file(sn=True, q=True)
    doc = Document()
    print scenename
    print posedic
    print Pose_name
    #root_node=doc.createElement('Posename: '+Pose_name+ '(filename: {0})'.format(scenename))
    root_node = doc.createElement('PoseData')
    doc.appendChild(root_node)
    file_node = doc.createElement('Filename')
    root_node.appendChild(file_node)
    file_node.setAttribute('FilePath', str(scenename))
    pose_node = doc.createElement('Posename')
    file_node.appendChild(pose_node)
    pose_node.setAttribute('PoseName', str(Pose_name))
    # print pose_controller
    for controller in data_class.keylist:
        controller_node = doc.createElement('Controller')
        pose_node.appendChild(controller_node)
        controller_node.setAttribute('Controller', str(controller))
        controllerAttr = maya.listAttr(
            controller, r=True, v=True, k=True, c=True)
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


def posesaver_pannel():
    maya.window(windowID, widthHeight=(
        500, 500), title='Pose Saver',s=True)
    form0=maya.formLayout('windowsform',p=windowID)
    layout = maya.columnLayout(layoutID,w=480)
    maya.formLayout(form0,e=True,af=[(layout,'top',10),(layout,'left',10),(layout,'right',10)])
    #maya.separator(p=form0)
    maya.text(l='Define the object that need to save pose',
              al='center', w=480, h=20, fn='boldLabelFont', p=layout)
    maya.columnLayout(w=480,h=50,cat=('left',50))
    maya.text(l='Data Name:',
              al='left', w=480, h=20, fn='boldLabelFont')
    maya.textField(textfieldID,pht='put the name here...', w=380,h=20)
    maya.setParent('..')
    maya.rowColumnLayout(
        w=480, h=35, nc=2, cs=[(1, 60), (2, 110), (3, 60)],rs=(1,5))
    maya.button(l='Add Data', w=125, h=30, al='center',c=constructdata)
    maya.button(l='Rename Data', w=125, h=30, al='center')
    maya.showWindow(windowID)


def rigginggui():
    if (maya.window(windowID, ex=True)):
        maya.deleteUI(windowID, wnd=True)
    posesaver_pannel()

rigginggui()
