import React from "react";
import cn from "classnames";

interface Props {
	slides: Object[];
	indexOfActiveSlide: number;
	size: Object;
	transparency?: boolean;
}

export default function (props: Props) {
	const getSlideStyle = (i: number) => {
		let index: number = i - props.indexOfActiveSlide - 1;
		if (index <= -2) index = props.slides.length + index;
		return {
			...props.size,
			left: `${100 * index}%`,
		};
	};

	const getActiveSlide = (i: number): boolean => {
		const index: number =
			props.indexOfActiveSlide < props.slides.length - 1 ? props.indexOfActiveSlide : -1;
		return index === i;
	};

	const animation = `carousel${
		props.transparency && props.slides.length > 3 ? "-transparent" : ""
	}`;
	let slides = [
		props.slides[props.slides.length - 1],
		...props.slides.slice(0, props.slides.length - 1),
	];

	while (slides.length <= 3) slides = slides.concat(slides);

	return (
		<div className="slider__wrapper" style={props.size}>
			{slides.map((slide, i) => (
				<div
					className={cn("slider__slide", `slider__slide_${animation}`, {
						[`slider__slide_${animation}_status_active`]: getActiveSlide(i - 1),
					})}
					key={i}
					style={getSlideStyle(i)}
				>
					{slide}
				</div>
			))}
		</div>
	);
}
