// this functino is working perfectly
/**
 * now what i want is, i have a languages object which is a list of {
        name: string;
        nativeName: string;
    }
  and the keys of the object are locale, i want to run this function for all of the keys on that object.
  it looks somthing like this: const languages: {
    ab: {
        name: string;
        nativeName: string;
    };
    aa: {
        name: string;
        nativeName: string;
    };
    af: {
        name: string;
        nativeName: string;
    };...}
    then at the end the script should write all of the result in a json file on the current director
 */
import languages from "./languages.js";
import fs from "fs";
function getNumerics(locale) {
  const numerics = [];

  const formatter = new Intl.NumberFormat(locale);
  for (let i = 0; i <= 9; i++) {
    const digits = formatter
      .formatToParts(i)
      .filter((part) => part.type === "integer" || part.type === "decimal");

    for (const digit of digits) {
      console.log(digit);
      numerics.push(digit.value);
    }
  }

  return numerics;
}

const result = {};
for (const locale in languages) {
  if (languages.hasOwnProperty(locale)) {
    const language = languages[locale];
    const numerics = getNumerics(locale);
    result[locale] = numerics;
  }
}

// Write the result to a JSON file
const jsonData = JSON.stringify(result, null, 2);
fs.writeFileSync("result.json", jsonData, "utf8");
