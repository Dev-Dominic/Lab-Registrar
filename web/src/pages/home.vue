<template>
<v-app> 
  <v-container>
    <v-row>
      <v-col lg="9">
    <v-app-bar  
      dark
      fixed
      elevate-on-scroll
      dense>
    <v-avatar><img src="../assets/multimedia.svg"></v-avatar>
    <v-toolbar-title>Digital Registrar</v-toolbar-title>
    <v-spacer></v-spacer>
          <v-toolbar-title><v-btn outlined class="mr-4"  @click="setToday">
            Today
          </v-btn></v-toolbar-title>
          <v-toolbar-title><v-btn fab text small  @click="prev">
            <v-icon small>mdi-chevron-left</v-icon>
          </v-btn></v-toolbar-title>
          <v-toolbar-title><v-btn fab text small  @click="next">
            <v-icon small>mdi-chevron-right</v-icon>
          </v-btn></v-toolbar-title>
          <v-toolbar-title>{{ title }}</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-toolbar-title><v-menu bottom right>
            <template v-slot:activator="{ on }">
              <v-btn
                outlined
                v-on="on"
              >
                <span>{{ typeToLabel[type] }}</span>
                <v-icon right>mdi-menu-down</v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item @click="type = 'day'">
                <v-list-item-title>Day</v-list-item-title>
              </v-list-item>
              <v-list-item @click="type = 'week'">
                <v-list-item-title>Week</v-list-item-title>
              </v-list-item>
              <v-list-item @click="type = 'month'">
                <v-list-item-title>Month</v-list-item-title>
              </v-list-item>
              <v-list-item @click="type = '4day'">
                <v-list-item-title>4 days</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu></v-toolbar-title>
        </v-app-bar>
  <v-row class="fill-height">
    <v-col>
      <v-sheet height="600">
        <v-calendar
          ref="calendar"
          v-model="focus"
          color="primary"
          :events="events"
          :event-color="getEventColor"
          :now="today"
          :type="type"
          @click:event="showEvent"
          @click:more="viewDay"
          @click:date="viewDay"
          @change="updateRange"
        ></v-calendar>
        <v-menu
          v-model="selectedOpen"
          :close-on-content-click="false"
          :activator="selectedElement"
          offset-x
        >
          <v-card
            color="grey lighten-4"
            min-width="350px"
            flat
          >
            <v-toolbar
              :color="selectedEvent.color"
              dark
            >
             
              <v-toolbar-title style="margin-left:4em" v-html="selectedEvent.name"></v-toolbar-title>
              <v-spacer></v-spacer>
            </v-toolbar>
            <v-card-text>
              <span style="font-weight:bold" >Lab Techs</span>
              <v-list v-for="labtech in selectedEvent.labtechs " :key="labtech">
                <span>{{labtech}}</span>
              </v-list>
            </v-card-text>
            <v-card-actions>
              <v-btn
                text
                color="secondary"
                @click="selectedOpen = false"
              >
                Close
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-menu>
      </v-sheet>
    </v-col>
  </v-row>
      </v-col>
      <v-col>
           <v-navigation-drawer
      absolute
      permanent
      right
      dark
    >
      <template v-slot:prepend>
        <v-list-item two-line>
          <v-list-item-avatar @click.stop="loggedin ? account_options = true : login_option = true" style="cursor:pointer" color="red">
            <span style="color:white;-webkit-touch-callout: none;-webkit-user-select: none;-khtml-user-select: none;-moz-user-select: none;-ms-user-select: none;user-select: none; 
">{{getInitials(first_name,last_name)}}</span>
          </v-list-item-avatar>

          <v-list-item-content>
            <v-list-item-title v-show="loggedin == false">None Logged In</v-list-item-title>
            <v-list-item-title v-show="loggedin == true">{{first_name}} {{last_name}}</v-list-item-title>
            <v-list-item-subtitle v-show="loggedin == true">Logged In</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </template>

      <v-divider></v-divider>
      <div class = "user_dashboard">
        <v-card width=245 style="margin-left:6px">
          <v-list-item two-line>
          <v-list-item-avatar width="70" height="70">
            <img @click="checkActiveSession" src="../assets/interface.svg">
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title>Active Session</v-list-item-title>
            <v-list-item-subtitle color="lightgray" style="font-weight:bold;">{{activeSession}}</v-list-item-subtitle>
            <digital-clock style="margin-top:1rem;font-weight:bold;font-size:24px" :blink="true"></digital-clock>
            <v-btn v-show="clockedIn == false" @click="confirm_login_option=true" height="20" style="margin-top:1rem">Clock In</v-btn>
            <v-btn v-show="clockedIn == true"  disabled height="20" style="margin-top:1rem">Clock In</v-btn>
          </v-list-item-content>
        </v-list-item>
        </v-card>
          <v-card width=245 style="margin-left:6px">
          <v-list-item two-line>
          <v-list-item-avatar width="70" height="70">
            <img src="../assets/business.svg">
          </v-list-item-avatar>

          <v-list-item-content>
            <v-list-item-subtitle style ="color:white">Friday, May 22nd</v-list-item-subtitle>
            <v-list-item-subtitle>12:00 a.m</v-list-item-subtitle>
            <v-list-item-subtitle color="lightgray">Next Shift</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        </v-card>
           <v-card width=245 style="margin-left:6px">
                 <v-list-item two-line>
          <v-list-item-avatar width="70" height="70">
            <img @click="swap_request_options=true" src="../assets/team.svg">
          </v-list-item-avatar>

          <v-list-item-content>
            <v-list-item-title>Labtechs on Duty</v-list-item-title>
            <v-list-item-subtitle style="font-weight:bold;font-size:36px;">{{labtechs_working}}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        </v-card>
      </div>
    </v-navigation-drawer>
      </v-col>
    </v-row>
    <v-dialog 
      v-model="account_options"
      max-width="265">
      <v-card>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="green darken-1"
            text
            @click="swap_request=true"
          >
            Swap Request
          </v-btn>
          <v-btn
            color="green darken-1"
            text
            @click="handleLogout"
          >
            Sign Out
          </v-btn>


        </v-card-actions>
      </v-card>
    </v-dialog>
        <v-dialog 
      v-model="swap_request_options"
      max-width="265">
      <v-card>
        <v-card-title style="margin-left:38px">Swap Requests</v-card-title>
        <v-card-actions>
          <v-list >
            <v-card v-for="request in swap_requests " :key="request.request_id" style="margin-left:38px;margin-bottom:10px">
            <v-card-title style="margin-left:5px">Time Slot ID: {{request.request_timeslot_id}}</v-card-title>
            <v-card-subtitle>{{request.labtech_request_id}}</v-card-subtitle>
            <v-btn
            color="green darken-1"
            text
            @click="confirmSwap(request.request_id)">Confirm</v-btn>
          </v-card>
          </v-list>
          <v-spacer></v-spacer>


        </v-card-actions>
      </v-card>
    </v-dialog>
        <v-dialog 
      v-model="login_option"
      max-width="265">
      <v-card>
        <v-card-actions>
          <v-spacer></v-spacer>
            <form>
    <v-text-field
      style="margin-top:40px"
      v-model="uwiIssuedID_login"
      :error-messages="selectErrors"
      label="UWI ID"
      required
      dense
      outlined
      shaped
      filled
      @change="$v.select.$touch()"
      @blur="$v.select.$touch()"
    ></v-text-field>
      <v-text-field
      v-model="password_login"
      :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
       @click:append="show1 = !show1"
      :items="items"
      :error-messages="selectErrors"
      label="Password"
      :type="show1 ? 'text' : 'password'"
      required
      filled
      dense
      shaped
      outlined
      @change="$v.select.$touch()"
      @blur="$v.select.$touch()"
    ></v-text-field>
              <v-btn
            color="green darken-1"
            text
            @click="handleLogin"
          >
            Login
          </v-btn>
  </form>


        </v-card-actions>
      </v-card>
    </v-dialog>
            <v-dialog 
      v-model="confirm_login_option"
      max-width="265">
      <v-card>
        <v-card-actions>
          <v-spacer></v-spacer>
            <form>
      <v-text-field
      v-model="confirm_password_login"
      style="margin-top:20px"
      :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
       @click:append="show1 = !show1"
      :items="items"
      :error-messages="selectErrors"
      label="Password"
      :type="show1 ? 'text' : 'password'"
      required
      filled
      dense
      shaped
      outlined
      @change="$v.select.$touch()"
      @blur="$v.select.$touch()"
    ></v-text-field>
              <v-btn
            color="green darken-1"
            text
            @click="clockIn"
          >
            Confirm
          </v-btn>
  </form>


        </v-card-actions>
      </v-card>
    </v-dialog>
       <v-dialog 
      v-model="swap_request"
      max-width="265">
      <v-card>
        <v-card-title style="margin-left:2.5rem">Swap Request</v-card-title>
        <v-card-actions>
          <form>
      <v-select
      v-model="select"
      :items="event_items"
      item-value="id"
      item-text="name"
      :error-messages="selectErrors"
      label="Session"
      required
      @change="$v.select.$touch()"
      @blur="$v.select.$touch()"
    ></v-select>
    <v-btn style="margin-left:9rem;" @click="handleSwapRequest">Send</v-btn>
  </form>
        </v-card-actions>
      </v-card>
    </v-dialog>
           <v-dialog 
      v-model="confirmSwap_diag"
      max-width="265">
      <v-card>
        <v-card-title style="margin-left:2.5rem">Swap Request</v-card-title>
        <v-card-actions>
          <form>
      <v-select
      v-model="select"
      :items="event_items"
      item-value="id"
      item-text="name"
      :error-messages="selectErrors"
      label="Session"
      required
      @change="$v.select.$touch()"
      @blur="$v.select.$touch()"
    ></v-select>
    <v-btn style="margin-left:9rem;" @click="swapConfirm">Send</v-btn>
  </form>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</v-app>
</template>

<script>
import DigitalClock from "vue-digital-clock"
import axios from 'axios'
  export default {
    components: {
    DigitalClock
  },
    data: () => ({
      confirmSwap_diag: false,
      request_id_active: null,
      swap_requests:[{   admin_approve_id: "",
    confirm_timeslot_id: "",
    labtech_confirm_id: "",
    labtech_request_id: "60000003",
    request_id: 1,
    request_timeslot_id: 3,
    status: "OPEN"}],
    swap_request_options:false,
      event_items:[],
      labtechs_active:null,
      labtechs_working: null,
      clockedIn:false,
      labtechs:null,
      confirm_login_option:false,
      activeSession: "",
      show1: false,
      login_option:false,
      focus: '',
      type: 'month',
      typeToLabel: {
        month: 'Month',
        week: 'Week',
        day: 'Day',
        '4day': '4 Days',
      },
      loggedin:false,
      swap_request: false,
      account_options: false,
      start: null,
      end: null,
      first_name: "",
      last_name: "",
      uwiID:null,
      selectedEvent: {},
      selectedElement: null,
      selectedOpen: false,
      events: [],
      colors: ['blue', 'indigo', 'deep-purple', 'cyan', 'green', 'orange', 'grey darken-1'],
    }),

    computed: {
 
      title () {
        const { start, end } = this
        if (!start || !end) {
          return ''
        }

        const startMonth = this.monthFormatter(start)
        const endMonth = this.monthFormatter(end)
        const suffixMonth = startMonth === endMonth ? '' : endMonth

        const startYear = start.year
        const endYear = end.year
        const suffixYear = startYear === endYear ? '' : endYear

        const startDay = start.day + this.nth(start.day)
        const endDay = end.day + this.nth(end.day)

        switch (this.type) {
          case 'month':
            return `${startMonth} ${startYear}`
          case 'week':
          case '4day':
            return `${startMonth} ${startDay} ${startYear} - ${suffixMonth} ${endDay} ${suffixYear}`
          case 'day':
            return `${startMonth} ${startDay} ${startYear}`
        }
        return ''
      },
      monthFormatter () {
        return this.$refs.calendar.getFormatter({
          timeZone: 'UTC', month: 'long',
        })
      },
    },
    mounted(){
    axios.get("http://localhost:5000/default/schedule/master").then((res)=>
    {
        var events_items = []
        var data_ = res.data
        for (var event_ in data_){
            events_items.push({
            name: data_[event_].event,
            id: event_
          })}
        this.event_items = events_items
    })
    axios.get("http://localhost:5000/default/labtech/working").then((res)=>
    {
      var size = Object.keys(res.data).length;
      this.labtechs_working = size
      this.labtechs_active = res.data
    })
    },
    methods: {
      swapConfirm(){
       var token = sessionStorage.getItem("token")
       var auth = "JWT " + token
       var config = {
          headers:{
            "Authorization": auth,
            "Content-Type": "application/json"
          }
        }  
      var jd = {
         "swap_request_id": this.request_id_active,
          "confirm_timeslot_id": this.select
      }  
      console.log(this.select,this.request_id_active)
      axios.patch("http://localhost:5000/web/request/swap/accept",jd,config).then((res) => {
          console.log(res.data.message)
          alert(res.data.message)  
        }).catch((err)=>{
          alert(err.data)
        })
      },
      confirmSwap(id){
        this.request_id_active = id
        this.confirmSwap_diag = true
      },
      getAllRequest(){
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
          if(data_[event_].status == "OPEN"){
            requests.push({
            admin_approve_id: data_[event_].admin_approve_id,
            confirm_timeslot_id: data_[event_].confirm_timeslot_id,
            labtech_confirm_id: data_[event_].labtech_confirm_id,
            labtech_request_id: data_[event_].labtech_request_id,
            request_id: data_[event_].request_id,
            request_timeslot_id: data_[event_].request_timeslot_id,
            status: data_[event_].status
          })}}
          this.swap_requests = requests})
      },
      getEventName(id){
        var name = "Blank"
           Array.from(this.event_items).forEach(event_ => {
            if(event_.id == id){
              console.log("works")
              name = event_.name
            }
          return name
          
        })
      },
      handleSwapRequest(){
        var token = sessionStorage.getItem("token")
        var auth = "JWT " + token
        var jd = {
          "request_labtech_timeslot_id" : this.select
        }
        var config = {
          headers:{
            "Authorization": auth,
            "Content-Type": "application/json"
          }
        }
      axios.post("http://localhost:5000/web/request/swap",jd,config).then((res) => {
          console.log(res.data.message)
          alert(res.data.message)  
        }).catch((err)=>{
          alert(err.data)
        })

      },
      clockIn(){
        var token = sessionStorage.getItem("token")
        var auth = "JWT " + token
        var jd ={	"uwiIssuedID": this.uwiID,
                  "password":this.confirm_password_login}
        var config = {
          headers:{
            "Authorization": auth,
            "Content-Type": "application/json"
          }
        }
        axios.post("http://localhost:5000/local/clockin",jd,config).then((res) => {
          console.log(res.data.clockin)
          if (res.data.clockin == true){
          this.confirm_login_option = false
          this.clockedIn = true
          alert("Successful clock-in")  
        }
        else{
          alert("This is not your timeslot")
        }}).catch((err)=>{console.log(err.data)})
      },
      checkActiveSession(){
        this.activeSession = this.getActiveSession(this.events)      },
     getActiveSession(events){
        var date = new Date()
        var name = "None Active"
        Array.from(events).forEach(event_ => {
          var date_ = new Date(event_.start)
          if ((date_.getHours() == date.getHours()) && (date_.getDay() == date.getDay())){
            name = event_.name
          }
        })
        return name
      },
      currentHour(string){
        var arr1 = string.split(" ")
        var arr2 = arr1[1].split(":")
        return arr2[0]
      },
      viewDay ({ date }) {
        this.focus = date
        this.type = 'day'
      },
      getEventColor (event) {
        return event.color
      },
      setToday () {
        this.focus = this.today
      },
      prev () {
        this.$refs.calendar.prev()
      },
      next () {
        this.$refs.calendar.next()
      },
      showEvent ({ nativeEvent, event }) {
        const open = () => {
          this.selectedEvent = event
          this.selectedElement = nativeEvent.target
          setTimeout(() => this.selectedOpen = true, 10)
        }

        if (this.selectedOpen) {
          this.selectedOpen = false
          setTimeout(open, 10)
        } else {
          open()
        }

        nativeEvent.stopPropagation()
      },
       updateRange ({ start, end }) {
        var events = []
        if (this.loggedin === false){
        var data_
        axios.get('http://localhost:5000/default/schedule/master').then((res) =>{
          data_ = res.data
        for (var event_ in data_){
            events.push({
            name: data_[event_].event,
            start: this.date_Converter(data_[event_].day,data_[event_].time),
            end: this.date_Converter(data_[event_].day,data_[event_].time+1),
            color: this.colors[this.rnd(0, this.colors.length - 1)],
            labtechs: data_[event_].labtechs
          })}})
   
          }
          else{
            events = this.getUserEvents()
          }
        this.start = start
        this.end = end
        this.events = events
      }, 
      nth (d) {
        return d > 3 && d < 21
          ? 'th'
          : ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th'][d % 10]
      },
      rnd (a, b) {
        return Math.floor((b - a + 1) * Math.random()) + a
      },
      formatDate (a, withTime) {
        return withTime
          ? `${a.getFullYear()}-${a.getMonth() + 1}-${a.getDate()} ${a.getHours()}:${a.getMinutes()}`
          : `${a.getFullYear()}-${a.getMonth() + 1}-${a.getDate()}`
      },
   
      date_Converter(weekday,time){
        var date = new Date()
        var currentDay = date.getDay();
        var distance = weekday - currentDay;
        date.setDate(date.getDate() + distance);
        date.setHours(time)
        date.setMinutes(0)
        return this.formatDate(date,time)
      },

      handleLogin(){
        var jd = {
          "uwiIssuedID": this.uwiIssuedID_login,
          "password": this.password_login
          }
          axios.post("http://localhost:5000/web/auth/login",jd).then((res) => {
            if("access_token" in res.data){
              let jwt_token = res.data.access_token
              sessionStorage.setItem('token',jwt_token)
            }}).finally(() =>{
              this.uwiID=this.uwiIssuedID_login
              console.log("Logged In")
              this.login_option=false
              this.userInfo()
              this.events = this.getUserEvents()
              this.loggedin = true
              this.getAllRequest()
            })
      },
      getInitials(name1,name2){
        if (name1 == "" && name2 == ""){
          return ""
        }
        var arr1 = name1.split("")
        var arr2 = name2.split("")
        return arr1[0] + arr2[0]
      },
      handleLogout(){
        sessionStorage.removeItem('token')
        console.log("Logged Out")
        this.loggedin = false
        this.account_options = false
        this.uwiID = null
        this.user = null
        this.first_name = ""
        this.last_name = ""
      },
      getUserEvents(){
        const events = []
        var token = sessionStorage.getItem("token")
        var auth = "JWT " + token
        var data_
        var config = {
          headers:{
            "Authorization": auth,
            "Content-Type": "application/json"
          },
          params:{	"uwiIssuedID": this.uwiID}
        }
        axios.get("http://localhost:5000/web/schedule",config).then((res) => {
        data_ = res.data
        for (var event_ in data_){
            events.push({
            name: data_[event_].event,
            start: this.date_Converter(data_[event_].day,data_[event_].time),
            end: this.date_Converter(data_[event_].day,data_[event_].time+1),
            color: this.colors[this.rnd(0, this.colors.length - 1)],
            labtechs: data_[event_].labtechs
          })
      }
        }) 
        return events
      },
       userInfo() {
        var token = sessionStorage.getItem("token")
        var auth = "JWT " + token
        var config = {
          headers:{
            "Authorization": auth,
            "Content-Type": "application/json"
          },
          params:{	"uwiIssuedID": this.uwiID}
        }
        axios.get("http://localhost:5000/web/user",config).then((res) => {
          this.first_name = res.data.firstname
          this.last_name = res.data.lastname
        }) 
     }
    }
    
    }
</script>
<style>
.user_dashboard > *{
  margin-top: 2rem;
}
</style>