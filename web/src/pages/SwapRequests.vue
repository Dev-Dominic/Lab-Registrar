<template>
<v-app>
  <v-card>
    <v-card-title>
      Users
      <v-spacer></v-spacer>
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
    <v-data-table
      :headers="headers"
      :items="swap_requests"
      :search="search"
      dark
    >
    <template v-slot:item.actions="{ item }">
      <v-btn v-show="item.status=='CONFIRM'"
        small
        color="green"
        class="mr-2"
        @click="adminApprove(item.request_id)"
      >
        CONFIRM
      </v-btn>
      <v-btn
      v-show="item.status=='CONFIRM'"
        color="red"
        small
        @click="adminDisapprove(item.request_id)"
      >
        DISAPPROVE
      </v-btn>
    </template></v-data-table>
  </v-card>
  
  </v-app>
</template>

<script>
import axios from 'axios'

  export default {
    data: () => ({
        search: '',
        headers: [
          { text: 'Requesting Lab Tech ID', sortable: true, value: 'labtech_request_id' },
          { text: 'Confirming Lab Tech ID', sortable: true ,value: 'labtech_confirm_id' },
          { text: 'Time Slot ID Requesting ', value: 'request_timeslot_id'},
          { text: 'Time Slot ID Confirming ', value: 'confirm_timeslot_id'},
            { text: 'Status ', value: 'status'},
          { text: 'Actions', value: 'actions'}
        ],
        swap_requests:[]
      }),
    created() {
        var token = sessionStorage.getItem("token")
        var auth = "JWT " + token
        var config = {
          headers:{
            "Authorization": auth,
            "Content-Type": "application/json"
          }
        }
      axios.get("http://localhost:5000/web/requests/swap",config).then((res) => {
        var data_ = res.data
        var requests = []
        for (var event_ in data_){
            requests.push({
            admin_approve_id: data_[event_].admin_approve_id,
            confirm_timeslot_id: data_[event_].confirm_timeslot_id,
            labtech_confirm_id: data_[event_].labtech_confirm_id,
            labtech_request_id: data_[event_].labtech_request_id,
            request_id: data_[event_].request_id,
            request_timeslot_id: data_[event_].request_timeslot_id,
            status: data_[event_].status
          })}
          this.swap_requests = requests})
      } ,
      methods:{
     adminApprove(id){
       var token = sessionStorage.getItem("token")
       var auth = "JWT " + token
       var config = {
          headers:{
            "Authorization": auth,
            "Content-Type": "application/json"
          }
        }  
      var jd = {
         "swap_request_id": id,
         "status": "APPROVED"
      }  
      console.log(id)
      axios.patch("http://localhost:5000/web/request/swap/approve",jd,config).then((res) => {
          console.log(res.data.message)
          alert(res.data.message)  
        }).catch((err)=>{
          console.log(err.data)
        })
      },
    adminDisapprove(id){
       var token = sessionStorage.getItem("token")
       var auth = "JWT " + token
       var config = {
          headers:{
            "Authorization": auth,
            "Content-Type": "application/json"
          }
        }  
      var jd = {
         "swap_request_id": id,
         "status": "DENIED"
      }  
      console.log(this.select,this.request_id_active)
      axios.patch("http://localhost:5000/web/request/swap/approve",jd,config).then((res) => {
          console.log(res.data.message)
          alert(res.data.message)  
        }).catch((err)=>{
          alert(err.data)
        })
      }
      }
        }
</script>