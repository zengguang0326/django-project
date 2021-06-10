let vm = new Vue({
    el:"#app",
    delimiters: ['[[', ']]'],
    data:{
        //v-model
        // 获取用户名
        username:"",
        // 获取密码
        password:"",
        // 获取确认密码
        password2:"",
        // 获取手机号
        mobile:"",
        // 获取是否勾选
        allow:"",
        // 获取图片验证码
        image_code:'',
        // 图片验证码路径
        image_code_url:"",
        // 保存图片验证码唯一标识符
        uuid:"",
        // 获取短信验证码
        sms_code:"",
        // 默认短信验证码提示
        sms_code_tip:"获取短信验证码",
        // v-show
        error_username:false,
        error_password:false,
        error_password2:false,
        error_mobile:false,
        error_allow:false,
        error_image_code:false,
        error_sms_code:false,

        //error-message
        // 默认用户名错误信息
        error_username_message:"",
        // 默认手机号错误信息
        error_mobile_message:"",
        // 默认图片验证码错误信息
        error_image_code_message:"",
        error_sms_code_message:"",
    },
    mounted(){
        this.get_image_code();
    },
    methods:{
        // 获取短信验证码
        get_sms_code(){
            // 避免重复点击
            if (this.sending_flag === true) {
                return;
            }
            this.sending_flag = true;

            // 校验参数
            this.check_mobile();
            this.check_image_code();
            if (this.error_mobile === true || this.error_image_code === true) {
                this.sending_flag = false;
                return;
            }
            let url = '/sms_codes/' + this.mobile + '/?image_code=' + this.image_code+'&uuid='+ this.uuid;
            axios.get(url,{
                responseType:'json'
            })
                .then(response=>{
                    if (response.data.code==='0'){
                        let num = 60;
                        let timer=setInterval(()=>{
                            if (num===1){
                                // 销毁计时器
                                clearInterval(timer);
                                this.sms_code_tip = "获取短信验证码";
                                this.sending_flag = false;

                        }else {
                                num-=1;
                                this.sms_code_tip = num+'秒'
                            }

                        },1000);


                    }else {
                        if (response.data.code == '4001') {
                        this.error_image_code_message = response.data.errmsg;
                        this.error_image_code = true;
                    } else { // 4002
                        this.error_sms_code_message = response.data.errmsg;
                        this.error_sms_code = true;
                    }
                    this.generate_image_code();
                    this.sending_flag = false;
                    }

                })
                .catch(error=>{
                    console.log(error.response)
                })
        },
        // 校验短信验证码
        check_sms_code(){
            if(this.sms_code.length===0){
                this.error_sms_code_message='请输入验证码';
                this.error_sms_code=true;

            }else {
                this.error_sms_code=false
            }
        },
        // 校验图片验证码
        check_image_code(){
            if(this.image_code.length!==4){
                this.error_image_code_message='验证码格式错误';
                this.error_image_code=true;

            }else {
                this.error_image_code=false
            }
        },
        // 获取图片验证码
        get_image_code(){
            this.uuid = generateUUID();
            this.image_code_url = '/image_codes/'+this.uuid+'/'
        },
        // 校验用户名
        check_username(){
            let re = /^[a-zA-Z0-9_-]{5,20}$/;
            if (re.test(this.username)){
                this.error_username = false;
            }else {
                this.error_username=true;
                this.error_username_message='请输入5-20个字符的用户名';
            }
            // 判断用户名是否满足正则表达式，如果满足在校验用户名是否重复
            if(this.error_username===false){
                // 进行用户名是否重复校验
                //axios 格式
                // axios.get('url','请求头').then(请求成功回调).catch(请求失败回调)
                let url = '/usernames/'+this.username+'/count/';
                axios.get(url,{
                    responseType:'json'
                })
                    .then(response =>{
                        if(response.data.count===1){
                            this.error_username=true;
                            this.error_username_message='用户名重复';
                        }else {
                            this.error_username=false
                        }
                    })
                    .catch(error=>{
                        console.log(error.response)
                    })
            }

        },
        // 校验密码
        check_password(){
            let re = /^[0-9A-Za-z]{8,20}$/;
            if (re.test(this.password)){
                this.error_password = false;
            }
            else {
                this.error_password=true;
            }

        },
        // 校验确认密码
        check_password2(){
            if(this.password !== this.password2) {
                this.error_password2 = true;
            } else {
                this.error_password2 = false;
            }

        },
        // 校验手机号
        check_mobile(){
            let re = /^1[3-9]\d{9}$/;
            if(re.test(this.mobile)) {
                this.error_mobile = false;
            } else {
                this.error_mobile_message = '您输入的手机号格式不正确';
                this.error_mobile = true;
            }
            // 如果手机格式满足条件
            if(this.error_mobile===false){
                // 使用axios发送ajax请求
                let url='/mobiles/'+this.mobile+'/count/';
                axios.get(url,{
                    responseType: 'json'
                })
                    .then(response=>{
                        if(response.data.count===1){
                            this.error_mobile=true;
                            this.error_mobile_message='手机号码重复';
                        }else {
                            this.error_mobile=false;
                        }
                    })
                    .catch(error=>{
                        console.log(error)
                })
            }

        },
        // 校验是否勾选协议
        check_allow(){
            if(!this.allow) {
                this.error_allow = true;
            } else {
                this.error_allow = false;
            }

        },
        // 监听表单提交事件
        on_submit(){
            this.check_username();
            this.check_password();
            this.check_password2();
            this.check_mobile();
            this.check_allow();

            if(this.error_name === true || this.error_password === true || this.error_password2 === true
            || this.error_mobile === true || this.error_allow === true) {
            // 禁用表单的提交
            window.event.returnValue = false;
        }

        },


    }
})