import requests
import time
import json
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


session = requests.Session()
session.trust_env = False
ip_address = "localhost" # Substitute with the IPv4 address of the PC running BPWin




placeholder = st.empty()


while(True):
   
   with placeholder.container():  
      # Machine Name
      try:
         response_machine_name = session.get(f"http://{ip_address}:8080/data/machine-name", timeout = 3)
         if (response_machine_name.status_code == 200):
            machine_name_map = json.loads(response_machine_name.text)
            st.session_state['machine_info'] = machine_name_map['Description'] + ": " + machine_name_map['Serial_Number']
      except:
         st.session_state['machine_info'] = "No Machine Info At This Time"


      # Current Job File Name, if loaded
      #
      try:
         response_current_job = session.get(f"http://{ip_address}:8080/data/job-name", timeout = 3)
         if (response_current_job.status_code == 200):
            current_job_map = json.loads(response_current_job.text)
            st.session_state['current_job'] = current_job_map['Path']
      except:
         st.session_state['current_job'] = "No Job Loaded At This Time"
         
      # Selected Device
      #
      try:
         response_selected_device = session.get(f"http://{ip_address}:8080/data/selected-device", timeout = 3)
         if (response_selected_device.status_code == 200):
            selected_device_map = json.loads(response_selected_device.text)
            st.session_state['selected_device'] = selected_device_map['Device']
      except:
         st.session_state['selected_device'] = "No Device Selected At This Time"




      # Job Statistics, including Machine Status, Yield, DPH, Light Tower Status,
      # Idle Time, Elapsed Time, Remaining Time,
      # Passed, Failed, Active and Remaining Devices
      #
      try:
         response_stats = session.get(f"http://{ip_address}:8080/data/job-stats", timeout = 3)
         if (response_stats.status_code == 200):
            job_stats_map = json.loads(response_stats.text)
            st.session_state['machine_status'] = job_stats_map['Machine_Status']
            st.session_state['job_yield'] = job_stats_map['Job_Yield']
            st.session_state['idle_time'] = job_stats_map['Idle_Time']
            st.session_state['elapsed_time'] = job_stats_map['Elapsed_Time']
            st.session_state['remaining_time'] = job_stats_map['Remaining_Time']
            st.session_state['device_passed'] = job_stats_map['Passed_Device']
            st.session_state['device_failed'] = job_stats_map['Failed_Device']
            st.session_state['device_active'] = job_stats_map['Active_Device']
            st.session_state['device_remaining'] = job_stats_map['Remaining_Device']


           
            light_tower_set = set()


            if (job_stats_map['Red_Light_On'] == "true"):
               light_tower_set.add('Red')
            if (job_stats_map['Amber_Light_On'] == "true"):
               light_tower_set.add("Amber")
            if (job_stats_map['Green_Light_On'] == "true"):
               light_tower_set.add('Green')  
            st.session_state['light_tower'] = light_tower_set
           
           
            job_dph_actual_list = st.session_state['job_dph_actual']
            job_dph_potential_list = st.session_state['job_dph_potential']


            job_dph_actual_list.append(job_stats_map['Actual_DPH'])
            job_dph_potential_list.append(job_stats_map['Potential_DPH'])


            if (len(job_dph_actual_list) > 10):
               job_dph_actual_list.pop(0)
               job_dph_potential_list.pop(0)


            st.session_state['job_dph_actual'] = job_dph_actual_list
            st.session_state['job_dph_potential'] = job_dph_potential_list
           
      except:
         st.session_state['machine_status'] = "No Machine Status At This Time"
         st.session_state['job_yield'] = "N/A"
         st.session_state['idle_time'] = "N/A"
         st.session_state['elapsed_time'] = "N/A"
         st.session_state['remaining_time'] = "N/A"
         st.session_state['device_passed'] = -1
         st.session_state['device_failed'] = -1
         st.session_state['device_active'] = -1
         st.session_state['device_remaining'] = -1
         st.session_state['light_tower'] = set()
         st.session_state['job_dph_actual'] = [0] * 10
         st.session_state['job_dph_potential'] = [0] * 10


   


      ##############################################################################
      # Arrange the Layout and Display all data
      #


      # The following section has 3 columns, with each column displaying the Red, Amber and Green light tower status
      #
      col_light_1, col_light_2, col_light_3 = st.columns(3)
      with col_light_1:
         if ('Red' in st.session_state['light_tower']):
            light_tower_placeholder_1 = st.error("Red light is on")
         else:
            light_tower_placeholder_1 = st.text("-")


      with col_light_2:
         if ('Amber' in st.session_state['light_tower']):
            light_tower_placeholder_2 = st.warning("Amber light is on")
         else:
            light_tower_placeholder_2 = st.text("-")


      with col_light_3:
         if ('Green' in st.session_state['light_tower']):
            light_tower_placeholder_3 = st.success("Green light is on")
         else:
            light_tower_placeholder_3 = st.text("-")


      # The following section has 2 columns. Display machine and device data
      #
      col_info_1, col_info_2 = st.columns(2)
      with col_info_1:
         machine_info_element = st.text(f"{st.session_state['machine_info']}")
         machine_status_element = st.text(f"{st.session_state['machine_status']}")


      with col_info_2:
         selected_device_element = st.text(f"{st.session_state['selected_device']}")
         current_job_element = st.text(f"{st.session_state['current_job']}")


      # The following section has 4 columns, displaying yield and time statistics
      #
      col_yield, col_idle_time, col_elapsed_time, col_remaining_time = st.columns(4)
      with col_yield:
         job_yield_element = st.metric(label="Job Yield", value=f"{st.session_state['job_yield']}")


      with col_idle_time:
         idle_time_element = st.metric(label="Idle Time", value=f"{st.session_state['idle_time']}")


      with col_elapsed_time:
         elapsed_time_element = st.metric(label="Elapsed Time", value=f"{st.session_state['elapsed_time']}")


      with col_remaining_time:
         remaining_time_element = st.metric(label="Remaining Time", value=f"{st.session_state['remaining_time']}")


      if(st.session_state['machine_status'] == "Active"):
         # The following section has 2 columns, displaying 2 charts, 1 for Device Statistics and the other for DPH
         #
         col_device_stats, col_dph = st.columns(2)
         with col_device_stats:
            st.subheader("Device Statistics")
            if (st.session_state['device_passed'] + st.session_state['device_failed'] <= 0):
               device_stats_element = st.text("There is no data available yet. ")
            else:
               df_device_stats = pd.DataFrame([['Passed', st.session_state['device_passed']], ['Failed', st.session_state['device_failed']], ['Remaining', st.session_state['device_remaining']]], columns=['Status', 'Quantity'])
               fig_device_stats = px.pie(df_device_stats, values='Quantity', names='Status', color='Status',
                     color_discrete_map={'Passed':'green',
                                       'Failed':'red',
                                       'Remaining':'gray'})
               fig_device_stats.update_traces(textinfo = 'value')
               device_stats_element = st.plotly_chart(figure_or_data=fig_device_stats, use_container_width=True, sharing="streamlit", theme="streamlit")


         with col_dph:
            st.subheader("DPH")
            job_dph_element = st.line_chart(data =
               pd.DataFrame(np.column_stack([st.session_state['job_dph_actual'], st.session_state['job_dph_potential']]),
                           columns = ['actual_dph', 'potential_dph']))
      time.sleep(0.1)


