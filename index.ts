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

// export const runFoo = async (runner: Runner, { fileName, args, env }: { fileName: string; args?: string; env?: Record<string, string> }) => {
//   run2(runner, fileName, args, env);
// };

const run = async (fileName: string, args?: string, env: Record<string, string> = {}) => {
  const arg = args || getArgs();
  const file = path.join(__dirname, "src", fileName);
  let command = `${pyInterpreter} -uB ${file}`;
  if (arg) command = `${command} ${arg}`;

  $`sh -c "${command}"`.env(env).catch((error: any) => {
    console.error(error.message);
  });
};

const execMap = {
  SOURCE_COMMONRC: "source ~/.commonrc",
};

type Runner = "python" | "bun" | "go";

const runnerMap: Record<Runner, { runScript: string; fileExt: string; srcDir: string }> = {
  python: { runScript: `${pyInterpreter} -uB`, fileExt: ".py", srcDir: "python" },
  bun: { runScript: "bun", fileExt: ".ts", srcDir: "src-ts" },
  go: { runScript: "go run", fileExt: ".go", srcDir: "go" },
};

export const run2 = async (runner: Runner, { fileName, args, preExecScript = [] }: { fileName: string; args?: string; preExecScript?: (keyof typeof execMap)[] }) => {
  if (!runnerMap[runner]) throw new Error(`Runner ${runner} not found`);

  const arg = args || getArgs();
  const file = path.join(__dirname, "src", runnerMap[runner].srcDir, fileName + runnerMap[runner].fileExt);
  let command = `${runnerMap[runner].runScript} ${file}`;
  if (arg) command = `${command} ${arg}`;

  const env: Record<string, string> = {};
  const defaultEnv = await $`sh -cl "bun -e 'console.log(JSON.stringify(process.env))'"`.json();
  for (const key in defaultEnv) env[key] = defaultEnv[key];

  for (const script of preExecScript) {
    const newEnv = await $`sh -cl "${execMap[script]} && bun -e 'console.log(JSON.stringify(process.env))'"`.json();
    for (const key in newEnv) env[key] = newEnv[key];
  }

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
