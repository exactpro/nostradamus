import { Tag, TagColor } from "app/common/components/charts/tag-cloud/types";
import { Terms } from "app/modules/significant-terms/store/types";

export class TagCloudGenerator {
	readonly MAX_SIZE = 20;
	readonly MIN_SIZE = 10;
	readonly AVAILABLE_COLORS = [TagColor.violet, TagColor.pink, TagColor.green, TagColor.yellow];

	private transformToList = (terms: Terms): Tag[] => {
		return Object.entries(terms)
			.map(([key, value]) => ({
				name: key,
				absoluteValue: value,
				relatedValue: value * 100,
				size: 0,
				color: this.AVAILABLE_COLORS[0],
			}))
			.sort((a, b) => b.relatedValue - a.relatedValue);
	};

	private generateRandomColorCollection = (lengthCollection: number): TagColor[] => {
		let result = new Array(lengthCollection);
		const countAvailableColors = this.AVAILABLE_COLORS.length;

		for (let i = 0; i < lengthCollection; i += 1) {
			result[i] = this.AVAILABLE_COLORS[i % countAvailableColors];
		}

		result = result.sort(() => Math.random() - 0.5);

		return result;
	};

	prepare = (terms: Terms) => {
		const result: Tag[][] = [[], [], [], []];

		const termsList: Tag[] = this.transformToList(terms);

		const colorsCollection = this.generateRandomColorCollection(termsList.length);

		const max: number = termsList[0].relatedValue;
		const min: number = termsList[termsList.length - 1].relatedValue;
		const step = (max - min) / (this.MAX_SIZE - this.MIN_SIZE);

		termsList.forEach(({ name, relatedValue, absoluteValue }, index) => {
			let size = this.MIN_SIZE + (relatedValue - min) / step;
			if (!size) size = (this.MAX_SIZE + this.MIN_SIZE) / 2;
			result[index % 4].push({
				name,
				relatedValue,
				absoluteValue,
				size,
				color: colorsCollection[index],
			} as Tag);
		});

		return result;
	};
}
