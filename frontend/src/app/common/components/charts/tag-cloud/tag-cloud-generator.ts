import { Tag, TagColor } from 'app/common/components/charts/tag-cloud/types';
import { Terms } from 'app/modules/significant-terms/store/types';

export class TagCloudGenerator {

	readonly MAX_SIZE = 20;
	readonly MIN_SIZE = 10;
	readonly AVAILABLE_COLORS = [TagColor.violet, TagColor.pink, TagColor.green, TagColor.yellow];

	private transformToList = (terms: Terms): Tag[] => {
		return Object.entries(terms).map(([key, value]) => ({
			name: key,
			value: value * 100,
			size: 0,
			color: this.AVAILABLE_COLORS[0],
		}));
	};

	private generateRandomColorCollection = (lengthCollection: number): TagColor[] => {
		let result = new Array(lengthCollection);
		const countAvailableColors = this.AVAILABLE_COLORS.length;

		for (let i = 0; i < lengthCollection; i++) {
			result[i] = this.AVAILABLE_COLORS[i % countAvailableColors];
		}

		result = result.sort(() => Math.random() - 0.5);

		return result;
	};

	prepare = (terms: Terms) => {
		let result: Tag[][] = [[], [], [], []];

		let termsList: Tag[] = this.transformToList(terms);

		let colorsCollection = this.generateRandomColorCollection(termsList.length);

		let
			max: number = termsList[0].value,
			min: number = termsList[termsList.length - 1].value;
		let step = (max - min) / (this.MAX_SIZE - this.MIN_SIZE);

		termsList.forEach(({ name, value }, index) => {
			let size = this.MIN_SIZE + (value - min) / step
			if(!size) size = (this.MAX_SIZE + this.MIN_SIZE)/2
			result[index % 4].push({
				name, value,size,
				color: colorsCollection[index],
			} as Tag);
		});

		return result;
	};

}