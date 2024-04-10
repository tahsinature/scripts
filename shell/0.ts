import { $ } from "bun";
import path from "path";

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

export const runLogin = async (fileName: string, args?: string) => {
  const env = await $`sh -cl "source ~/.commonrc && bun -e 'console.log(JSON.stringify(process.env))'"`.json();
  await run(fileName, args, env);
};

export const runNonLogin = async (fileName: string, args?: string) => {
  const env = await $`sh -cl "bun -e 'console.log(JSON.stringify(process.env))'"`.json();
  await run(fileName, args, env);
};

const run = async (fileName: string, args?: string, env: Record<string, string> = {}) => {
  const arg = args || getArgs();
  const { pyInterpreter, file } = getPaths(fileName);
  let command = `${pyInterpreter} -uB ${file}`;
  if (arg) command = `${command} ${arg}`;

  $`sh -c "${command}"`.env(env).catch((error: any) => {
    console.error(error.message);
  });
};
