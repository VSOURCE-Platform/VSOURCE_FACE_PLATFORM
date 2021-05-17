import React from 'react'
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
        $.ajax({
          url: 'http://localhost:12349/login',
          type:'post',
          xhrFields: {
            withCredentials: true,
          },
          headers: {
            "Access-Control-Allow-Origin": "*"
          },
          crossDomain: true,
          dataType:'json',
          data:{
              username:$("#email-address").val(),
              password:$("#password").val()
          },
          success:function (data) {
              if(data.status == 200){
                  window.location.href = '/';
                  console.log('login success!');
              }else{
                  console.log('login fail!');
                  $("#login_status").text("Invalid username or password!");
              }
              console.log(data)
          },
          error:function (error) {
            $("#login_status").text("Login Error!");
          }
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

export default LoginPage;