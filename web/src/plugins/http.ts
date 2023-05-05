import axios from "axios";
import { AxiosError , AxiosRequestConfig } from 'axios'
import Vue from 'vue'
import store from "@/store";
import createAuthRefreshInterceptor from 'axios-auth-refresh';
import {AxiosAuthRefreshOptions} from 'axios-auth-refresh';
import moment from 'moment-timezone'

function setTokenTimeout(data){
    // console.log(data)
    let remainingTime = null
    if(data?.session_time && data?.token_time && Number(data?.token_expiry)){
        const sessionTime = moment(data.session_time)        
        const tokenExpiry = Number(data.token_expiry)
        const expiryTime = sessionTime.add(tokenExpiry,'seconds')
        const currentTime = moment().utc()
        const tokenTime = moment(data.token_time).utc()
        remainingTime = moment.duration(expiryTime.diff(tokenTime)).asSeconds()
        console.log(remainingTime)
        console.log(currentTime.format())
        console.log(tokenTime.format())
    }
    store.commit('Common/setSessionExpiry',remainingTime)    
}

const refreshAuthLogic = failedRequest => axios.get('/token').then(response => {
    if (response.status == 200 && response.data.access_token == null) {
        location.replace(response.data.login_url);
        return Promise.resolve();
    }
    store.commit('Common/setToken',response.data.access_token);
    store.commit('Common/setLogoutUrl',response.data.logout_url)
    setTokenTimeout(response.data)
    // store.commit('CommonInformation/setTokenExpiry',response.data.expires_at);
    if (failedRequest != null)
        failedRequest.response.config.headers['Authorization'] = 'Bearer ' + response.data.access_token;
    return Promise.resolve();
}).catch((error: AxiosError) => {
    console.error(error);
});

const options: AxiosAuthRefreshOptions = {
    statusCodes: [ 401, 403]
}

function successInterceptor(config: AxiosRequestConfig) {
    // async 

    //     if (!config.url?.endsWith('/token') && new Date() > new Date(store.state.CommonInformation.tokenExpiry))
    //     {
    //         console.log("Refreshing token, without 401.");
    //         await refreshAuthLogic(null);
    //     }
    const token = store.state.Common.token;    
    config.headers['Authorization'] = 'Bearer ' + token; 
  
    return config;
}

function configureInstance(){
    createAuthRefreshInterceptor(axios, refreshAuthLogic, options);    

    axios.interceptors.request.use(successInterceptor);    
    axios.defaults.baseURL = process.env.BASE_URL +'api/v1'
    return axios;    
}

const httpInstance = configureInstance();

export default {
    install () {
        Vue.prototype.$http = httpInstance
    }
};

