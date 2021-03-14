import { createGlobalStyle } from "styled-components";
import reset from "styled-reset";

const globalStyle = createGlobalStyle`
    ${reset};
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    @font-face {
        font-family: "Binggrae";
        src: url("BinggraeMelona.ttf") format("truetype");
        font-style: normal;
        font-weight: normal;
    }

    a {
        text-decoration: none;
        color: inherit;
    }

    body {
        background-color: #222831;
        width: 100%;
        min-height: 100%;
        font-family: 'Roboto', sans-serif;
    }
`;

export default globalStyle;
