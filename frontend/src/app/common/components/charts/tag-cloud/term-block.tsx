import cn from "classnames";
import React, { useEffect, useRef, useState } from "react";

interface TermBlockProps {
	name: string;
	shortName: string;
	value: string;
	color: string;
	size: number;
	screenCoefficient: number;
	zIndex: number;
}

export default function TermBlock(props: TermBlockProps) {
	const [isHovered, setHoverStatus] = useState<boolean>(false);
	const [termSize, setTermSize] = useState({ width: 0, height: 0 });
	const termRef = useRef<HTMLDivElement>(null);
	useEffect(() => {
		if (termRef.current) {
			const termRectSize = termRef.current.getBoundingClientRect();
			setTermSize({ width: termRectSize.width, height: termRectSize.height });
		}
	}, [props.size, props.screenCoefficient]);

	const standardSize = 12;
	const fullTermTitleCoefficient = isHovered
		? props.shortName.length / (props.name.length + 0.5 * props.value.length)
		: 1;

	return (
		<div
			ref={termRef}
			onMouseMove={() => setHoverStatus(true)}
			onMouseLeave={() => setHoverStatus(false)}
			className={cn("tag-cloud__term", `tag-cloud__term_color_${props.color}`)}
			style={{
				fontSize: Math.floor(
					(props.size || standardSize) * props.screenCoefficient * fullTermTitleCoefficient
				),
				padding: isHovered ? 0 : "0 1em",
				zIndex: 10 - props.zIndex,
				width: isHovered ? termSize.width : "",
				height: isHovered ? termSize.height : "",
			}}
		>
			<span>{isHovered ? props.name : props.shortName}</span>
			{isHovered && <span>&nbsp;{props.value}</span>}
		</div>
	);
}
