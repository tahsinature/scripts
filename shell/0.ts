#!/Users/mohammadtahsin/.bun/bin/bun
// @ts-nocheck

import { $ } from "bun";
import path from "path";

const executors = {
  login: path.join(__dirname, "0-login"),
  nonLogin: path.join(__dirname, "0-non-login"),
};

const getPaths = (fileName: string) => {
  return {
    pyInterpreter: path.join(__dirname, "..", ".venv", "bin", "python3"),
    file: path.join(__dirname, "..", "src", fileName),
  };
};

// [ "--question", "test" ] => "--question test"
// [ "--question", "test", "--answer", "test" ] => "--question test --answer test"
// [ "--exec" ] => "--exec"
// [ ] => ""
// [ "echo hi" ] => """echo hi"""
const getArgs = () => {
  const args = process.argv.slice(2).map((ele) => {
    if (ele.includes(" ")) {
      return `"""${ele}"""`;
    }
    return ele;
  });

  return args.join(" ");
};

export const runLogin = async (fileName: string) => {
  run(executors.login, fileName);
};

export const runNonLogin = async (fileName: string) => {
  run(executors.nonLogin, fileName);
};

const run = async (executor: string, fileName) => {
  const arg = getArgs();
  const { pyInterpreter, file } = getPaths(fileName);
  let command = `${executor} ${pyInterpreter} -B ${file}`;
  if (arg) command = `${command} ${arg}`;

  await $`bash -c "${command}"`.catch((error: any) => {
    console.error(error.message);
  });
};
