import React, { useReducer } from "react";
import "./App.css";
import styled, { createGlobalStyle } from "styled-components";
import { Route } from "react-router-dom";

import NavBar from "./components/NavBar/NavBarContainer";
import Main from "./components/Main/MainContainer";
import Capture from "./components/Capture/CaptureContainer";
import Logic from "./components/Logic/LogicContainer";
import Community from "./components/Community/CommunityContainer";
import SelectIngredients from "./components/SelectIngredients/SIContainer";
import WritePost from "./components/Community/WritePost/WritePostContainer";
import Detail from "./components/Community/Detail/DetailContainer";

const GlobalStyle = createGlobalStyle`
  body{
    font-family : 'NanumSquare';

    -ms-user-select: none; 
    -moz-user-select: -moz-none;
    -khtml-user-select: none;
    -webkit-user-select: none;
    user-select: none;
  }
`;

const Container = styled.div`
  max-width: 767px;
  margin: 0 auto;
`;
const initialState = {
  uid: "",
  searchMode: false

}
const reducer = (state, action) => {

  switch (action.type) {
    case 'SET_UID':
      return {
        ...state,
        uid: action.uid
      };

    case 'SET_SEARCHMODE':
      return {
        ...state,
        searchMode: action.mode
      };

    default:
      return state;
  }

}

export const store = React.createContext(initialState);

function App () {
  const [state, dispatch] = useReducer(reducer, initialState);
  const { searchMode } = state;

  return (
    <store.Provider value={{ state, dispatch }}>
      <GlobalStyle />
      {searchMode ? null : <NavBar />}

      <Container>
        <Route exact path="/" component={Main} />
        <Route exact path="/selectIngredients" component={SelectIngredients} />
        <Route exact path="/capture" component={Capture} />
        <Route exact path="/logic" component={Logic} />
        <Route exact path="/community" component={Community} />
        <Route exact path="/community/write" component={WritePost} />
        <Route exact path="/community/detail/:pid" component={Detail} />

      </Container>
    </store.Provider>
  );
}

export default App;
