export type Tag = {
	name: string,
	absoluteValue: number,
	relatedValue: number,
	size: number,
	color: TagColor
}

export enum TagColor {
	violet = 'violet',
	pink = 'pink',
	green = 'green',
	yellow = 'yellow',
}
