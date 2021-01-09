import pytesseract
from PIL import Image
import re
import requests

ID = 'rv-Zbq_EFiKNDPyL8HZ02YbaMiDzMw4K'
model_ID = '9e1e33b4-5e47-45f3-8bd8-e900999e2f52'


def main():
    
    '''
    url = 'https://app.nanonets.com/api/v2/OCR/Model/'+ model_ID +'/LabelFile/'
    data = {'file': open('.\OCR\DSC_0238.JPG', 'rb')}
    response = requests.post(url, auth=requests.auth.HTTPBasicAuth(ID, ''), files=data)
    response=response.json()
    predict_result = response['result'][0]['prediction'][0]['ocr_text']
    '''
    print('----------------------------')
    #current_date = input('Please input current date(ex.20110304)：')
    current_date = 20221201
    data_now=list(str(current_date))
    current_date=list(str(current_date))
    current_date.insert(4,'.') 
    current_date.insert(7,'.')
    current_date=''.join(current_date)
    
    print('Today is', current_date)
     
    #predict_result='2021 01 09'
    #predict_result='2021/01/09'
    #predict_result='2021.01.09/12:08'
    #predict_result='E20220518 1D 02694 10:48 L..'
    #predict_result='製造 1100101 有效 1101130'
    predict_result='製造 1091201 有效 1101130'
    #predict_result='製造 20210101 有效 20211130'      
    
    
    Fetch_date=[]
    test_list=[]    
    print('=========== Strating prediction.....')
    print('Input string = ',predict_result)
    for i in predict_result:
        if re.match(r'[0-9]',i):
            test_list.append(i)
    test_list=''.join(test_list)    
     
    cnt=1
    if len(test_list)>8:
        cnt=2
    
    for itr in range(cnt):    
        Date1=re.match(r'202.',test_list)
        Date2=re.match(r'11.',test_list)
        Date3=re.match(r'10.',test_list)
        if Date1:
            Fetch_date.append(test_list[Date1.span(0)[0]:Date1.span(0)[1]+4])
            #print('Fetch_date',Fetch_date)
            test_list=test_list[:Date1.span(0)[0]]+test_list[Date1.span(0)[1]+4:]
        elif Date2:
            New_date = int(test_list[Date2.span(0)[0]:Date2.span(0)[1]+4])
            New_date = New_date + 19110000            
            Fetch_date.append(str(New_date))
            #print('Fetch_date',Fetch_date)
            test_list=test_list[:Date2.span(0)[0]]+test_list[Date2.span(0)[1]+4:]
        elif Date3:
            New_date = int(test_list[Date3.span(0)[0]:Date3.span(0)[1]+4])
            New_date = New_date + 19110000            
            Fetch_date.append(str(New_date))            
            #print('Fetch_date',Fetch_date)
            test_list=test_list[:Date3.span(0)[0]]+test_list[Date3.span(0)[1]+4:]    
        #print('test_list',test_list)
    
    #print('Date list =',Fetch_date)    
    l_date = Fetch_date[0]
    for date in Fetch_date:
        if int(date)>int(l_date):
            l_date=date
    
    #Date compare if 2 date
    ####Note data_now=list(str(current_date))
    date_product=list(l_date)       
    
    l_date=list(l_date)
    l_date.insert(4,'.') 
    l_date.insert(7,'.')
    l_date=''.join(l_date)
    print('Last data=',l_date )
    print('=========== Finish Prediction.....')
        
    date_now_y = int(data_now[1]+data_now[2]+data_now[3])
    date_product_y = int(date_product[1]+date_product[2]+date_product[3])
    compare_year = date_product_y - date_now_y
    print('')    
    if compare_year>=0:
        compare_month = (compare_year*12+int(date_product[4]+date_product[5]))-int(data_now[4]+data_now[5])
        if compare_month>=0:
            compare_day =(compare_month*30 + int(date_product[6]+date_product[7]))-int(data_now[6]+data_now[7])
            if compare_day>=0:
                print('Days to expire is %d-D'%(compare_day))
            else:
                print('Warning !!! produce expired days =',abs(compare_day))            
        else:
            print('Warning !!! produce expired over few days')
    else:
        print('Warning !!! produce expired over month')   
    print('----------------------------')     
    print('')    
 

if __name__ == "__main__":
    main()


