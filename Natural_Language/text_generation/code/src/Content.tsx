import React, { FC, useState } from "react";
import { Card, Button } from "@veneer/core";
import TextArea from "./TextArea";
import TextBox from "./TextBox";

type ResponseType =
  | undefined
  | {
      predictions: string;
    };

function wait(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

const Content: FC = () => {
  const [loading, setLoading] = useState(false);
  const [initialWord, setInitialWord] = useState<string>("");
  const [size, setSize] = useState<string>("120");

  const [output, setOutput] = useState<ResponseType>(undefined);

  const submit = async (): Promise<void> => {
    setLoading(true);
    const requestBody = {
      inputs: {
        initial_word: [initialWord],
        size: [Number(size)],
      },
      params: {
        show_score: true,
      },
    };
    try {
      const response = await fetch("/invocations", {
        method: "POST",
        headers: {
          "Content-Type": "application/json;charset=UTF-8",
        },
        body: JSON.stringify(requestBody),
      });
      const json = await response.json();
      setOutput(json);
      // await wait(2000);
      // setOutput({
      //   predictions: "To be or not to be, that is the question.",
      // });
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex size-full flex-row justify-evenly p-8 pt-0">
      <div className="flex h-full w-1/3 flex-col gap-20 pl-8 pr-4">
        <Card
          border="outlined"
          className="relative flex h-full flex-col justify-center"
          content={
            <TextArea
              placeholder="Initial words"
              title="Initial words"
              value={initialWord}
              onChange={(value) => setInitialWord(value)}
            />
          }
        />
        <Card
          border="outlined"
          className="relative flex h-full flex-col justify-center"
          content={
            <TextBox
              placeholder="Size"
              title="Size"
              type="number"
              value={size}
              onChange={(value) => setSize(value)}
            />
          }
        />
      </div>
      <div className="flex w-1/6 flex-col  justify-center">
        <Button
          appearance="primary"
          disabled={loading || initialWord === "" || size === ""}
          trailingIcon={
            loading ? (
              <div className="ml-3">
                <div className="spinner" />
              </div>
            ) : (
              <div />
            )
          }
          onClick={submit}
        >
          {loading ? "Submitting" : "Submit"}
        </Button>
      </div>
      <div className="h-full w-1/3 pl-4 pr-8">
        <Card
          border="outlined"
          className="flex h-full flex-col justify-center"
          content={
            <div>
              <TextArea
                className="h-auto pb-0"
                placeholder="Output"
                title="Output"
                value={output?.predictions || ""}
                readOnly
              />
            </div>
          }
        />
      </div>
    </div>
  );
};

export default Content;
