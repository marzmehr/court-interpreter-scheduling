<template>
    <header name="navigation-topbar" class="app-header">

        <nav class="navbar navbar-expand-lg navbar-dark">

            <div class="container-fluid">

                <a class="navbar-brand"
                    href="https://www2.gov.bc.ca"
                    style="max-width: 200px">
                    <img class="img-fluid d-none d-md-block"
                        src="../images/bcid-logo-rev-en.svg"
                        width="177"
                        height="44"
                        alt="B.C. Government Logo"/>

                    <img class="img-fluid d-md-none"
                        src="../images/bcid-symbol-rev.svg"
                        width="63"
                        height="44"
                        alt="B.C. Government Logo"/>

                </a>

                <div class="navbar-brand navbar-text">                    
                    Court Interpreter Scheduling                  
                </div>

                <div class="navbar-extra">
                    <div id="app-profile">
                        <div v-if="userName" style="padding-right: rem">
                            <b-row>
                                <b-col>
                                    <b-dropdown id="profileDropdown"
                                                text="Profile"
                                                variant="primary btn-transparent"
                                                menu-class="w-10"
                                                >
                                        <template #button-content >
                                            <span class="fa fa-user"></span> {{ userName }}
                                        </template>
                                        <b-dropdown-item @click="logout()">
                                            <b-icon-box-arrow-left class="mr-2"/>Logout
                                        </b-dropdown-item>                                
                                    </b-dropdown>
                                </b-col>
                                <b-col>
                                    <b-form-select
                                        v-model="userCourtLocation"                                        
                                        @change="ChangeUserLocation()" 
                                        >
                                        <b-form-select-option value=null>
                                            --- Remove Location ---
                                        </b-form-select-option>
                                        <b-form-select-option
                                            v-for="location in sortedCourtLocations" 
                                            :key="location.id"
                                            :value="location.id">
                                                {{location.name}}
                                        </b-form-select-option>

                                    ></b-form-select>
                                    
                                </b-col>                                
                                <b-alert style="margin-top:0.8rem" :variant="alertType" :show="dismissCountDown"  @dismissed="dismissCountDown=0" @dismiss-count-down="countDownChanged">
                                    <b v-if="alertType=='success'">Saved <b-icon-check-square-fill/> </b>
                                    <b v-else>Error <b-icon-exclamation-circle-fill/> </b>
                                </b-alert>
                            </b-row>                          

                        </div>
                    </div>
                </div>

                <div v-if="sessionTime" id="app-exit" class="app-exit">
                    <b-card no-body
                        :class="sessionClass">
                        <b-row class="m-0">
                            <span><b-icon-stopwatch scale="1.2" /></span>
                            <span class="ml-2">{{sessionMin}}' {{sessionSec}}"</span>
                        </b-row>
                    </b-card>
                </div>

                <button class="navbar-toggler"
                    type="button"
                    data-toggle="collapse"
                    data-target="#navbarNavAltMarkup"
                    aria-controls="navbarNavAltMarkup"
                    aria-expanded="false"
                    aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
            </div>
            
        </nav>
        
    </header>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import { SessionManager } from "@/components/utils/utils";
import { locationsInfoType } from "@/types/Common/json";
import * as _ from 'underscore';

import { namespace } from "vuex-class";   
import "@/store/modules/common";
const commonState = namespace("Common");

@Component
export default class NavigationTopbar extends Vue {
    
    @commonState.State
    public userName!: string;

    @commonState.State
    public courtLocations!: locationsInfoType[];
    
    @commonState.State
    public userLocation!: locationsInfoType;
    
    @commonState.Action
    UpdateUserLocation!: (newUserLocation: locationsInfoType) => void

    @commonState.State
    public sessionExpiry!: number;

    userCourtLocation: number =0;

    dismissCountDown =0
    alertType=""

    timeHandle1
    sessionTime=0
    sessionMin=0
    sessionSec=""
    sessionClass=""

    @Watch('courtLocations')
    UserNameChange() 
    {
        this.userCourtLocation = this.userLocation?.id
    }

    @Watch('sessionExpiry')
    sessionExpiryChange()
    {
        if(this.sessionExpiry){
            clearTimeout(this.timeHandle1);
            this.sessionTime=Number(this.sessionExpiry)
            setTimeout(this.getUpdatingInfo, 1);
        }
    }

    mounted(){
        this.userCourtLocation = this.userLocation?.id 
        this.sessionExpiryChange()
    }

    public getUpdatingInfo(){                
        
        
        if(this.sessionTime>300) 
            this.sessionClass="text-success"
        else 
            this.sessionClass="text-danger"
        
        clearTimeout(this.timeHandle1);
        if(this.sessionTime>1){
            this.sessionTime--;
            this.sessionMin = Math.floor(this.sessionTime/60)
            const sessionSec = (this.sessionTime%60)
            this.sessionSec = sessionSec<10 ? ('0'+sessionSec) : String(sessionSec)
            this.timeHandle1 = window.setTimeout(this.getUpdatingInfo, 1000);
        }else if(this.sessionTime==1){
            this.logout()
        }       
    }

    public logout() {
        clearTimeout(this.timeHandle1);
        SessionManager.logout(this.$store);
    }

    public ChangeUserLocation(){
        Vue.nextTick(()=>{
            let data = {
                "locationId": this.userCourtLocation
            }

            if(!data.locationId || (String(data.locationId)=='null') )
                data = {} as {"locationId": number}


            this.$http.put('/user-info/save-location', data).then(res=>{
                // console.log(res)
                this.alertType="success"
                this.dismissCountDown = 1;
                const newUserCourtLocation = (this.courtLocations.filter(loc=>{return loc.id == this.userCourtLocation}))
                if(newUserCourtLocation.length==1)
                    this.UpdateUserLocation(newUserCourtLocation[0])
            },error => {
                this.alertType="danger"
                this.dismissCountDown = 1;
                this.userCourtLocation = this.userLocation?.id
            })
        })
    }

    public countDownChanged(dismissCountDown) {
        this.dismissCountDown = dismissCountDown
    }

    get sortedCourtLocations(){
        return _.sortBy(this.courtLocations,'name')
    }

}
</script>

<style>
.btn-transparent {
  background-color: transparent !important;
  border-color: #ccc !important;
}
</style>

<style scoped lang="scss">
@import "../styles/common";
.navbar {
  padding-right: 170px;
}
.navbar-brand:not(.logo) {
  flex: 1 1 auto;
}
.navbar-extra {
  display: inline-block;
  flex: 1 1 auto;
  text-align: right;
}
.navbar .navbar-extra {
  display: inline-block;
  flex: 1 1 auto;
  text-align: right;
}

#app-profile {
  color: $gov-white;
}

#app-exit {
    padding: 8px 15px;
    position: absolute;
    position: fixed;
    right: 0;
    top: 0;
    z-index: 100;
    .card {
        border-radius: 1rem;
        font-size: 110%;
        font-weight: 600;
        padding: 0.5rem 1rem;
    }
}

.alert{
    font-weight: 800;
    height: 2.4rem;
    margin:0;
    padding: 0.4rem 1rem;
}
</style>