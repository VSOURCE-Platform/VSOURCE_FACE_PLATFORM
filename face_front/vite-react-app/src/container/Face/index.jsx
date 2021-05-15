import React from 'react'
import axios from 'axios'
import $ from 'jquery';
import my_logo from '../Index/logo.png';

class LoginTitle extends React.Component {
    render() {
        return <div>
        <img className="mx-auto h-12 w-auto" src={my_logo} alt="Workflow"/>
        <h2 className="mt-2 text-center text-3xl font-extrabold text-gray-900">Sign in to your account</h2>
        <h4 id="login_status" className="mt-2 text-center font-extrabold text-red-900"></h4>
        </div>
    }
}

class EmailInput extends React.Component {
    render() {
        return <div>
          <label for="email-address" className="sr-only">Email address</label>
          <input id="email-address" type="email" autocomplete="email" required className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" placeholder="Email address"/>
        </div>
    }
}

class PasswordInput extends React.Component {
    render() {
        return <div>
          <label for="password" className="sr-only">Password</label>
          <input id="password" type="password" autocomplete="current-password" required className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" placeholder="Password"/>
        </div>
    }
}

class InputBlock extends React.Component {
    render() {
        return <div className="rounded-md shadow-sm -space-y-px">
          <EmailInput />
          <PasswordInput />
        </div>
    }
}

class RememberMeBlock extends React.Component {
    render() {
        return <div className="flex items-center">
              <input id="remember_me" name="remember_me" type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" />
              <label for="remember_me" className="ml-2 block text-sm text-gray-900" >
                Remember me
              </label>
            </div>
    }
}

class RegisterBlock extends React.Component {
    render() {
        return <div className="text-sm"><a href="#" class="font-medium text-indigo-600 hover:text-indigo-500">Forgot your password?</a>
            </div>
    }
}

class BottomBlock extends React.Component {
    render() {
        return <div className="flex items-center justify-between">
            <RememberMeBlock />
            <RegisterBlock />
        </div>
    }
}

class SignInButton extends React.Component {
    constructor(props) {
        super(props);
        this.state = {isSubmit: false};
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick() {
        axios({
            method: "post",
            url: "/app/login",
            withCredentials:true,
            data: {username:$("#email-address").val(),password:$("#password").val()},
            headers: {"Access-Control-Allow-Origin": "*",'Content-Type': 'application/x-www-form-urlencoded'}
            }
        ).then(res=>{
           console.log(res.data);
           if (res.data.status == 400){
                $("#login_status").append("用户名或密码错误");
//                 _this.setState({isLoaded:false});
           }else {
                window.location.reload();
//                 _this.setState({isLoaded:true});
           }
        },
        error=>{
          console.log('失败了',error);
        });
    }

    render() {
        return <div>
            <button onClick={this.handleClick} id="submitBtn" type="submit" className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">Sign in</button>
        </div>
    }
}

class LoginForm extends React.Component {
    render() {
        return <div className="mt-8 space-y-6" action="#" method="POST">
           <InputBlock />
           <BottomBlock />
           <SignInButton />
        </div>
    }
}

class LoginSecondPage extends React.Component {
    render() {
        return <div className="max-w-md w-full space-y-8">
          <LoginTitle />
          <LoginForm />
        </div>
    }
}


class LoginPage extends React.Component {
    render() {
        return <div className="min-h-screen flex items-center justify-center bg-gray-20 py-12 px-4 sm:px-6 lg:px-8">
          <LoginSecondPage />
        </div>
    }
}

class Face extends React.Component {
    constructor(props){
        super(props);
        this.state={
            isLoaded:false
        }
    }
    componentDidMount(){
        const _this=this;    //先存一下this，以防使用箭头函数this会指向我们不希望它所指向的对象。
        axios.get('http://localhost:12349/is_login').then(res=>{
           console.log(res.data);
           if (res.data.status == 400){
                _this.setState({isLoaded:false});
           }else {
                _this.setState({isLoaded:true});
           }
        },
        error=>{
          console.log('失败了',error);
        });
    }

    render() {
        if (this.state.isLoaded){
            return <div> Face Page </div>
        }else{
            return <LoginPage />
        }
    }
}

export default Face;