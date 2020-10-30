import React from "react";
import cn from "classnames";

interface Props {
	slides: Object[];
	indexOfActiveSlide: number;
	size: Object;
	transparency?: boolean;
}

export default function (props: Props) {
	const getSlideStyle = (i: number) => ({
		...props.size,
		left: `${100 * (i - props.indexOfActiveSlide)}%`,
	});

	const animation = `slider${props.transparency ? "-transparent" : ""}`;

	return (
		<div className="slider__wrapper" style={props.size}>
			{props.slides.map((slide, i) => (
				<div
					className={cn(
						"slider__slide",
						`slider__slide_${animation}`,
						props.indexOfActiveSlide === i && `slider__slide_${animation}_status_active`
					)}
					key={i}
					style={getSlideStyle(i)}
				>
					{slide}
				</div>
			))}
		</div>
	);
}
