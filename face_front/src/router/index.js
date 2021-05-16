// router/index.js
import Index from '../container/Index'
import Face from '../container/Face'

const routes = [
  {
    path: "/",
    component: Index
  },
  {
    path: "/face",
    component: Face
  }
];

export default routes