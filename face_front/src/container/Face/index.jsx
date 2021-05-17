import React from 'react'
import $ from 'jquery';
import my_logo from '../Index/logo.png';
import LoginPage from '../LoginPage'
import FacePage from '../FacePage'

import TableDemo from './Components/table'

class Face extends React.Component {
    constructor(props){
        super(props);
        this.state={
            isLoaded:true
        }
    }
    componentDidMount(){
        const _this=this;    //先存一下this，以防使用箭头函数this会指向我们不希望它所指向的对象。
        $.ajax({
          url: 'http://localhost:12349/is_login',
          type:'get',
          xhrFields: {
            withCredentials: true,
          },
          headers: {
            "Access-Control-Allow-Origin": "*"
          },
          crossDomain: true,
          success:function (data) {
              if(data.status == 200){
                  _this.setState({isLoaded:true});
              }else{
                  _this.setState({isLoaded:false});
              }
              console.log(data)
          },
          error:function (error) {
              _this.setState({isLoaded:false});
          }
        });
    }

    render() {
        if (this.state.isLoaded){
            return <FacePage />
        }else{
            return <LoginPage />
        }
    }
}

export default Face;