export type ChartsList = Chart[];

export interface Chart {
  name: string,
  data: ChartData
}

export type ChartData = ChartItemData[];

export interface ChartItemData {
  name: string,
  value: number
}
