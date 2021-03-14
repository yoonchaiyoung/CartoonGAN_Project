import Header from "./Header";
import Home from "../Routes/Home";
import Login from "../Routes/Login";
import CreateAccount from "../Routes/CreateAccount";
import Cartoon from "../Routes/Cartoon";
import Gallery from "../Routes/Gallery";
import Filter from "../Routes/Filter";
import { HashRouter, Switch, Route } from "react-router-dom";

const Router = () => {
  return (
    <>
      <HashRouter>
        <Header />

        <Switch>
          <Route path="/" exact component={Home} />
          <Route path="/filter" exact component={Filter} />
          <Route path="/cartoon" exact component={Cartoon} />
          <Route path="/gallery" exact component={Gallery} />
          <Route path="/login" exact component={Login} />
          <Route path="/login/createAccount" exact component={CreateAccount} />
        </Switch>
      </HashRouter>
    </>
  );
};

export default Router;
