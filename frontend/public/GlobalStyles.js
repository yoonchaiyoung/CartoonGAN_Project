import { createGlobalStyle } from "styled-components";
import reset from "styled-reset";

const globalStyle = createGlobalStyle`
    ${reset};
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: Binggrae;
        color: white;
    }

    a {
        text-decoration: none;
        color: inherit;
    }

    @font-face {
        font-family: "Binggrae";
        src: url("BinggraeMelona.ttf") format("truetype");
        font-style: normal;
        font-weight: normal;
    }
`;

export default globalStyle;
