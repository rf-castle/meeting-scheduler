<template>
    <div class="candidate_wrapper">
        <div class="empty_times">
            <div class="empty_time" v-for="(empty_time, date) in empty_times">
                <h3>{{ date }}</h3>
                <p><input type="checkbox" v-model="data">{{ empty_time }}</p>
                
            </div>
        </div>
        <div class="submit_wrapper">

        </div>
    </div>
</template>
<script lang="ts">
import Vue from 'vue'
import axios from 'axios'

export default Vue.extend({
    props:["companyName"],
    data(){
        return {
            empty_times: {},
            data:[]
        }
    },  
    mounted(){
        this.getEmptyTimes()
        
    },
    methods:{
        getEmptyTimes(){
            const url = "http://localhost:9000/empty-dates"
            axios.get(url).then((response) => {
                console.log(response.data)
                console.log(typeof(response.data))
                this.empty_times = response.data
            });
            this.preprocess()
        },
        preprocess(){
            console.log(Object.keys(this.empty_times))
            let processed_list: any = []
            Object.keys(this.empty_times).forEach((key: string) => {
                // this.empty_times[key].forEach((empty_time => {
                //     processed_list.push(key + " " + empty_time)
                // }))
                console.log(key)
            })
            console.log(processed_list)
            this.empty_times = processed_list
        },  
        submitCandidate(){
            console.log(this.data)
        }
    }
})
</script>
