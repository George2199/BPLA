import{_ as u,B as p}from"./Botinokbar-DOa3B7WN.js";import{a as g,A as m}from"./api-Ck5ob5MO.js";import{r as h,e as v,f as w,c as l,o as t,a as s,F as i,g as k,h as f,i as _,j as x,t as y,n as C,k as b,_ as B,l as c}from"./index-xRVBzM9d.js";const Q={class:"container"},j={class:"card-image-wrapper"},L=["alt","src"],M={class:"card-text"},$={class:"progress-wrapper"},F={__name:"CoursesIcons",setup(n){const o=h([]);return v(async()=>{try{const r=await g.get("/courses");o.value=r.data}catch(r){console.error("\u274C \u041D\u0435 \u0443\u0434\u0430\u043B\u043E\u0441\u044C \u0437\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044C \u043A\u0443\u0440\u0441\u044B:",r)}}),(r,e)=>{const d=w("router-link");return t(),l(i,null,[e[1]||(e[1]=s("svg",{width:"0",height:"0"},[s("defs",null,[s("mask",{id:"cutout-mask",maskContentUnits:"objectBoundingBox"},[s("rect",{x:"0",y:"0",width:"1",height:"1",fill:"white"}),s("path",{d:`
          M 0 0
          Q 0 0.18, 0 0.28
          Q 0 0.18, 0.05 0.18
          L 0.46 0.18
          Q 0.50 0.18, 0.50 0.13
          L 0.50 0.05
          Q 0.50 0, 0.55 0
          L 0 0
          Z
        `,fill:"black"})])])],-1)),s("div",Q,[(t(!0),l(i,null,k(o.value,a=>(t(),f(d,{key:a.id,class:"card",to:`/courses/${a.id}`},{default:_(()=>[s("div",j,[s("img",{class:"card-image",alt:a.title,src:`${x(m)}${a.image_url}`},null,8,L),e[0]||(e[0]=s("div",{class:"card-arrow"},[s("svg",{xmlns:"http://www.w3.org/2000/svg",class:"arrow-icon",fill:"none",viewBox:"0 0 24 24",stroke:"currentColor","stroke-width":"2"},[s("circle",{cx:"12",cy:"12",r:"10",fill:"white"}),s("path",{stroke:"#7C6EF2",d:"M8 16l8-8M10 8h6v6","stroke-linecap":"round","stroke-linejoin":"round"})])],-1))]),s("div",M,y(a.title),1),s("div",$,[s("div",{class:b(["progress-bar",a.progress,"progress-bar-gradient"]),style:C({width:a.progress*100+"%"})},null,6)])]),_:2},1032,["to"]))),128))])],64)}}},I={class:"app-container"},A={class:"main-content"},E={__name:"Courses",setup(n){return(o,r)=>(t(),l("div",I,[s("div",A,[c(u),c(F),c(p)])]))}},U=B(E,[["__scopeId","data-v-72c6d1c0"]]);export{U as default};
