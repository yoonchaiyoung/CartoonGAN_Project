import React from "react";
import styled, { keyframes } from "styled-components";

const a1 = keyframes`
    to {
       transform: rotate(360deg); 
    }
`;

const a2 = keyframes`
    to {
        transform: rotate(-360deg);
    }
`;

const LoadingContainer = styled.div`
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: ${(props) => (props.usage === "transfer" ? "center" : "none")};
  margin-top: ${(props) => (props.usage === "transfer" ? "10px" : "10rem")};

  div.loading {
    width: 200px;
    height: 200px;
    border-radius: 50%;
    border-top: 10px solid #e74c3c;
    position: relative;

    display: flex;
    justify-content: center;
    align-items: center;

    animation: ${a1} 2s linear infinite;

    span {
      color: white;
      animation: ${a2} 2s linear infinite;
    }
  }

  div.loading::before,
  div.loading::after {
    content: "";
    width: 200px;
    height: 200px;
    position: absolute;
    left: 0;
    top: -10px;
    border-radius: 50%;
  }

  div.loading::before {
    border-top: 10px solid #e67e22;
    transform: rotate(120deg);
  }

  div.loading::after {
    border-top: 10px solid #3498db;
    transform: rotate(240deg);
  }

  @media screen and (max-width: 378px) {
    margin-top: ${(props) => (props.usage === "transfer" ? "10px" : "5rem")};
  }
`;

const Loading = ({ text, usage }) => {
  return (
    <LoadingContainer usage={usage}>
      <div className="loading">
        <span>{text}</span>
      </div>
    </LoadingContainer>
  );
};

export default Loading;
