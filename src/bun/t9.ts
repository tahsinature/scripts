import meow from "meow";
import { askBoolean, askText } from "./utilities/prompt";

const cli = meow(
  `
	Usage
	  $ t9 --text <word> --single
    Options
      --text, -t  Word to convert to T9
      --single, -s  Return single digits
    Examples
      $ t9 --text "hello" --single
      43556
`,
  {
    importMeta: import.meta,
    flags: {
      text: {
        type: "string",
      },
      single: {
        type: "string",
        choices: ["true", "false"],
        default: "true",
      },
    },
  }
);

const wordToT9 = (word: string, returnSingle: boolean = true) => {
  const t9: Record<string, number> = {
    a: 2,
    b: 22,
    c: 222,
    d: 3,
    e: 33,
    f: 333,
    g: 4,
    h: 44,
    i: 444,
    j: 5,
    k: 55,
    l: 555,
    m: 6,
    n: 66,
    o: 666,
    p: 7,
    q: 77,
    r: 777,
    s: 7777,
    t: 8,
    u: 88,
    v: 888,
    w: 9,
    x: 99,
    y: 999,
    z: 9999,
    " ": 0,
  };

  return word
    .split("")
    .map((letter) => {
      const num = t9[letter.toLowerCase()];
      if (returnSingle) return num.toString().charAt(0);
      return num;
    })
    .join(returnSingle ? "" : "-");
};

const { text, single } = cli.flags;

const userInput = text || (await askText());
const isSingle = single ? single === "true" : await askBoolean();
const result = wordToT9(userInput, isSingle);

console.log(`The T9 representation of ${userInput} is ${result}`);
