import React from 'react'
import my_logo from './logo.png';

function Title(){
    return <h1 className="mt-6 text-2xl font-bold sm:text-xl">
        Hi, there. Please choose a service.
    </h1>
}

function ImageDiv(){
    return <img className="h-20 py-3" src={my_logo} />
}

export default function Index() {
  return <body className="bg-gray-20">
    <ImageDiv />
    <div className="p-40">
    <Title />
    <div className="mt-6 mx-auto">
        <a className="btn-primary" href="/face">Face Service</a>
        <a className="btn-secondary m-2" href='#'>Demo</a>
    </div>
</div>
</body>
}