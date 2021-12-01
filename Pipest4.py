import streamlit as st
import requests as r
import pandas as pd
import time

st.title("Banabikurye Outbound Deal Yaratma Aracı")
st.subheader("Aşağıdaki formda yer alan tüm bilgileri doldurtuktan sonra 'Create Deal' butonuna basınız.")



with st.form(key='my_form'):
    org_name = st.text_input('Organization name')
    org_region = st.text_input('Region')
    org_email = st.text_input('Email')
    org_phone = st.text_input('Phone')
    org_phone2 = st.text_input('Other Phone')
    legal_type = st.radio("Legal type", ("Business", "Individual", "No answer"))
    del_est = st.radio("Delivery estimation", ("5'den fazla", "5'den az", "Individual"))
    industry = st.selectbox("Industry", ('Autos / Parts & Services', 'Beauty & Fitness', 'Bevarages', 'Cakes & Bakeries', 'Consumer Electronics / Accessories', 'Courier Lead', 'Dental Products', 'Documents', 'E-Commerce', 'Fashion & Lifestyle', 'Flowers', 'Food - Fresh Products', 'Food - Restaurant', 'Gifts & Souvenir', 'Grocery', 'Grocery - Pet Products', 'Healthcare / Pharmacy', 'Individuals', 'Laundry Services', 'Media & Communication', 'No Answer/ No Response', 'Optics', 'Others', 'Supermarket'))
    notes = st.text_input("Notes")
    lost_reason = st.selectbox("Lost reason", ('High Price', 'Service Issues', 'In House Courier', 'Same Day Delivery not Required', 'Different Logistics Need', 'Thermal Bag Requirement', 'Can not reach/No Response', 'Courier Lead', 'Delivery Services not required', 'Wrong lead - Outside service area', 'Wrong Lead - Individual', 'Has another active DV account'))
    submit_button = st.form_submit_button(label='Create Deal')
    
if submit_button:
   st.subheader("Teşekkürler")
   
#create organization func
def create_org(org_name, org_email, org_phone, org_region):
    organization = {'owner_id':11539544,
            "name": org_name,
           "b1faf8cf25454aa8690d7b761def5b29be2c9b07": org_email,
           "d3ace2189605037b38016a44957b190f45a924b9": org_phone,
           "208c219904faba22afb629d63d1c9b89c516cd13": org_region,
           "visible_to": '5'}
    org = r.post("https://api.pipedrive.com/v1/organizations?api_token=st.secrets['token']", json=organization)
    result_1 = org.json()
    org_id = result_1["data"]["id"]
    return(org_id)

#create person func
def create_person(org_name, org_email, org_phone, org_region, org_id):
    person = {'owner_id':11539544,
              "org_id": org_id,
              "name": org_name,
             'phone': [{'label': 'work', 'value': org_phone, 'primary': True}],
              'email': [{'label': 'work',
              'value': org_email,
              'primary': True}],
             "0507562a28a905fbe5917476d9b800fbf7dc1bdd": org_region,
               'visible_to': '5'
    }
    per = r.post("https://api.pipedrive.com/v1/persons?api_token=st.secrets['token']", json=person)
    result_1 = per.json()
    per_id= result_1["data"]["id"]
    return(per_id)


if legal_type == 'Individual':
   org_id = create_org(org_name, org_email, org_phone, org_region)
   person_id = create_person(org_name, org_email, org_phone, org_region, org_id)
   deal = {"user_id": 11539544,
            "title": org_name+" Deal",
            "org_id": org_id,
            "person_id": person_id,
            "visible_to": '5',
            "stage_id": 163,
            "status": 'lost',
            "pipeline_id": 24,
            "3a662cbe0cfc0973a1eea76537b9c7515597f853": "TR Outsource Outbound",
            "17da88af586cac66b9aca3f151bf3dbc33b48ba7": 104, #legal type
            "fbe218c1b8ec237d98c16f6f618ab3f8407c0718": 464, #industry
            "89512fda9a0ecb6eae1c93acffaaf1decdd2647b": 226,
            "lost_reason": "Wrong Lead - Individual",
            "label": 992}
   deals = r.post("https://api.pipedrive.com/v1/deals?api_token=st.secrets['token']", json=deal)
   result_2 = deals.json()
   deal_id=result_2["data"]["id"]
   st.write("Deal ID: ", deal_id)
   act = {"deal_id": deal_id,
       "person_id": person_id,
       "org_id": org_id,
       "note": notes+" "+org_phone2,
       "user_id": 11539544,
        "done": 1}
   actt = r.post("https://api.pipedrive.com/v1/activities?api_token=st.secrets["token"]", json=act)
   res = actt.json()
   st.write(res["success"])
elif legal_type == "No answer":
   org_id = create_org(org_name, org_email, org_phone, org_region)
   person_id = create_person(org_name, org_email, org_phone, org_region, org_id)
   deal = {"user_id": 11539544,
            "title": org_name+" Deal",
            "org_id": org_id,
            "person_id": person_id,
            "visible_to": '5',
            "stage_id": 163,
            "status": 'lost',
            "pipeline_id": 24,
            "3a662cbe0cfc0973a1eea76537b9c7515597f853": "TR Outsource Outbound",
            "17da88af586cac66b9aca3f151bf3dbc33b48ba7": 460,
            "fbe218c1b8ec237d98c16f6f618ab3f8407c0718": 466, 
            "89512fda9a0ecb6eae1c93acffaaf1decdd2647b": 226,
            "lost_reason": "Can not reach/No Response",
            "label": 992}
   deals = r.post("https://api.pipedrive.com/v1/deals?api_token=st.secrets["token"]", json=deal)
   result_2 = deals.json()
   deal_id=result_2["data"]["id"]
   st.write("Deal ID: ", deal_id)
   act = {"deal_id": deal_id,
       "person_id": person_id,
       "org_id": org_id,
       "note": notes+" "+org_phone2,
       "user_id": 11539544,
        "done": 1}
   actt = r.post("https://api.pipedrive.com/v1/activities?api_token=st.secrets["token"]", json=act)
   res = actt.json()
   st.write(res["success"])
elif legal_type == "Business":
   org_id = create_org(org_name, org_email, org_phone, org_region)
   person_id = create_person(org_name, org_email, org_phone, org_region, org_id)
   deal = {"user_id": 11539544,
            "title": org_name+" Deal",
            "org_id": org_id,
            "person_id": person_id,
            "visible_to": '5',
            "stage_id": 297,
            "status": 'open',
            "pipeline_id": 3,
            "3a662cbe0cfc0973a1eea76537b9c7515597f853": "TR Outsource Outbound",
            "17da88af586cac66b9aca3f151bf3dbc33b48ba7": 105, #legal type
            "fbe218c1b8ec237d98c16f6f618ab3f8407c0718": industry, 
            "89512fda9a0ecb6eae1c93acffaaf1decdd2647b": 226,
            "label": 992}
   deals = r.post("https://api.pipedrive.com/v1/deals?api_token=st.secrets["token"]", json=deal)
   result_2 = deals.json()
   deal_id=result_2["data"]["id"]
   st.write("Deal ID: ", deal_id)
   act = {"deal_id": deal_id,
       "person_id": person_id,
       "org_id": org_id,
       "note": "Notlar: "+notes+" Other phone:"+org_phone2+" Estimated dels: "+del_est,
       "user_id": 11539544,
        "done": 1}
   actt = r.post("https://api.pipedrive.com/v1/activities?api_token=st.secrets["token"]", json=act)
   res = actt.json()
   st.write(res["success"])
else:
    st.write("hiçbir şey olmamışsa bile bir şey olmuş olabilir")
