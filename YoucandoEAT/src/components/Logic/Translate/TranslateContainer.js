import React, { useState, useCallback } from "react";
import TranslatePresenter from "./TranslatePresenter";
import axios from "axios";
import ipObj from "../../../key";

function TranslateContainer () {
    const [inputs, setInputs] = useState("");
    const [outputs, setOutputs] = useState("");

    const onChangeInputs = useCallback(
        (e) => {
            setInputs(e.target.value)
        },
        []
    );

    const clickEnter = () => {
        if (inputs === "") return;

        axios
            .get(`${ipObj.ip}/translate?text=${inputs}`)
            .then((response) => {
                console.log("url:", "GET /translate", "\nstatus:", response.status, "\nstatusText:", response.statusText);
                var translated = response.data.message.result.translatedText;
                setOutputs(translated);
            })
            .catch((err) => {
                console.error(err.response);
            });
    };

    return (
        <>
            <TranslatePresenter
                inputs={inputs}
                output={outputs}
                onChangeInputs={onChangeInputs}
                clickEnter={clickEnter} />
        </>
    );
}
export default React.memo(TranslateContainer);
