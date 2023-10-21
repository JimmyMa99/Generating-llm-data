import pandas as pd
import json  
import copy

def get_student_info(excel_path='data/student_info.xlsx'):

    student_info={}

    df=pd.read_excel(excel_path)
    for index,row in df.iterrows():
        student_info[row['姓名']]={}
        student_info[row['姓名']]['性别']=row['性别']
        student_info[row['姓名']]['年龄']=row['年龄']
        student_info[row['姓名']]['爱好']=row['爱好']

    return student_info

def make_prompt(student_info):
    data={
            "conversation": [  
            {  
                "input": "",  
                "output": ""  
            }  
        ] 
    }
    data_list=[]

    base_knowledge='你需要记得，班里有{}个同学，他们分别是{}。相近的爱好容易让他们更加相处更加融洽。'.format(len(student_info),','.join(student_info.keys()))
    base_response='好的，我记住了，我能够理解他们的爱好，比如喜欢爬山的和喜欢游泳的，都喜欢运动，他们之间的话题就会更多，而喜欢看书的和喜欢看电影的，都喜欢文艺，他们之间的话题也会更多。'
    data['conversation'][0]['input'],data['conversation'][0]['output']=base_knowledge,base_response
    data_dict_hardcopy=copy.deepcopy(data)
    data_list.append(data_dict_hardcopy)

    for name in student_info:
        gender=student_info[name]['性别']
        age=student_info[name]['年龄']
        hobby=student_info[name]['爱好']

        base_sample='你好，我是{}，我今年{}岁，我喜欢{}。'.format(name,age,hobby)
        base_response='同学{}你好，我是班主任，很高兴认识你。'.format(name)

        reverse_sample='你好{}，很高兴认识你。'.format(name)
        reverse_response='老师你好，我是{}，我今年{}岁，我喜欢{}。'.format(name,age,hobby)

        more_input=['请你描述一下{}。'.format(name),
                    '{},你今年多大了？'.format(name),
                    '{},你喜欢什么？'.format(name),]
        if gender=='男':
            more_response=['{}是一名{}岁的男同学,喜欢{}。'.format(name,age,hobby),
                            '{}今年{}岁了。'.format(name,age),
                            '{}喜欢{}。'.format(name,hobby),]
        else:
            more_response=['{}是一名{}岁的女同学，喜欢{}。'.format(name,age,hobby),
                            '{}今年{}岁了。'.format(name,age),
                            '{}喜欢{}。'.format(name,hobby),]
        input_list=[base_sample,reverse_sample]+more_input
        response_list=[base_response,reverse_response]+more_response
        
        for input,response in zip(input_list,response_list):
            data['conversation'][0]['input'],data['conversation'][0]['output']=input,response
            data_dict_hardcopy=copy.deepcopy(data)
            data_list.append(data_dict_hardcopy)
        print(data_list)
    return data_list

def save_json(data_list,json_path='results/data.json'):

    with open(json_path,'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)
        
        

 
        

if __name__=='__main__':
    student_info=get_student_info()
    data_list=make_prompt(student_info)
    save_json(data_list)