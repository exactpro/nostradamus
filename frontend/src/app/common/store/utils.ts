// description of this solution you can find here https://habr.com/ru/company/alfa/blog/452620/ (rus)
export type InferValueTypes<T> = T extends { [key: string]: infer U } ? U : never;
