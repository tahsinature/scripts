import prompts from "prompts";

export const askText = async () => {
  return prompts({
    type: "text",
    name: "text",
    message: "Enter a word",
  }).then((response) => response.text);
};

export const askBoolean = async ({ defaultValue = true }: { defaultValue?: boolean } = {}) => {
  return prompts({
    type: "confirm",
    name: "boolean",
    message: "Return single digits?",
    initial: defaultValue,
  }).then((response) => response.boolean);
};
