import Home from './components/Home.vue'
import Student_signup from './components/Student_signup.vue'
import Student_login from './components/Student_login.vue'
import Instructor_signup from './components/Instructor_signup.vue'
import Instructor_login from './components/Instructor_login.vue'
import InstructorDashboard from './components/InstructorDashboard.vue'
import CreateProject from './components/CreateProject.vue'
import StudentDashboard from './components/StudentDashboard.vue'
import InstructorViewProject from './components/InstructorViewProject.vue'


import {createRouter, createWebHistory} from 'vue-router'

const routes=[
    {
        name:'Home', 
        component:Home,
        path:'/'
    },
    {
        name:'Student_signup', 
        component:Student_signup,
        path:'/student_signup'
    },
    {
        name:'Student_login', 
        component:Student_login,
        path:'/student_login'
    },
    {
        name:'StudentDashboard', 
        component:StudentDashboard,
        path:'/student_dashboard'
    },
    {
        name:'Instructor_signup', 
        component:Instructor_signup,
        path:'/instructor_signup'
    },
    {
        name:'Instructor_login', 
        component:Instructor_login,
        path:'/instructor_login'
    },
    {
        name:'InstructorDashboard', 
        component:InstructorDashboard,
        path:'/instructor_dashboard'
    },
    {
        name:'CreateProject', 
        component:CreateProject,
        path:'/create_project'
    },
    {
        name:'InstructorViewProject', 
        component:InstructorViewProject,
        path:'/instructor_view_project'
    }
];

const router=createRouter({
    history:createWebHistory(),
    routes
});

export default router
