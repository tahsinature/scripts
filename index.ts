import { $ } from "bun";
import path from "path";

const pyInterpreter = path.join(__dirname, ".venv", "bin", "python3");

export const checkDependencies = async () => {
  const systemPython = {
    version: (await $`python --version`.text()).trim(),
    path: await $`which python`.text(),
  };

  const venvPython = {
    version: (await $`${pyInterpreter} --version`.text()).trim(),
    path: pyInterpreter,
  };

  console.log("System Python:", systemPython);
  console.log("Venv Python:", venvPython);

  await $`which node && which bun && which gum && which python3 && which fzf`;
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
  const file = path.join(__dirname, "src", fileName);
  let command = `${pyInterpreter} -uB ${file}`;
  if (arg) command = `${command} ${arg}`;

  $`sh -c "${command}"`.env(env).catch((error: any) => {
    console.error(error.message);
  });
};

export const test = async () => {
  const command = `${pyInterpreter} -Bm unittest`;

  await $`sh -c "${command}"`.catch((error: any) => {
    console.error(error.message);
  });
};
