import { TagCloudGenerator } from "app/common/components/charts/tag-cloud/tag-cloud-generator";
import { Tag } from "app/common/components/charts/tag-cloud/types";
import Tooltip from "app/common/components/tooltip/tooltip";
import { Terms } from "app/modules/significant-terms/store/types";
import cn from "classnames";
import React from "react";

import "./tag-cloud.scss";

interface IProps {
	tags: Terms;
	className?: string;
	percentage?: boolean;
}

export class TagCloud extends React.Component<IProps> {
	getShortVersion(termName: string): string {
		if (termName.length > 9) {
			return `${termName.slice(0, 8)}...`;
		}
		return termName;
	}

	getScreenSizeCoefficient = () => {
		if (window.screen.width < 1600) return 1;
		else if (window.screen.width >= 1600 && window.screen.width < 1920) return 1600 / 1280;
		else return 1920 / 1280;
	};


	renderBlock = (termsList: Tag[], position: string) => {
		const standardSize = 12;
		const screenCoefficient = this.getScreenSizeCoefficient();

		return (
			<div className={cn("tag-cloud__block", position)}>
				{termsList.map(({ name, size, absoluteValue, color }, index) => (
					<div
						key={name}
						className={cn("tag-cloud__term", `tag-cloud__term_color_${color}`)}
						style={{ fontSize: Math.floor((size || standardSize)*screenCoefficient), zIndex: 10 - index }}
					>
						<Tooltip
							duration={1}
							message={`${name} - ${absoluteValue.toFixed(1)}${this.props.percentage ? "%" : ""}`}
						>
							{this.getShortVersion(name)}
						</Tooltip>
					</div>
				))}
			</div>
		);
	};

	render() {
		const tagList = new TagCloudGenerator().prepare(this.props.tags);

		return (
			<div className={cn("tag-cloud", this.props.className)}>
				<div className="tag-cloud__row">
					{this.renderBlock(tagList[0], "top-left")}
					{this.renderBlock(tagList[2], "top-right")}
				</div>
				<div className="tag-cloud__row">
					{this.renderBlock(tagList[3], "bottom-left")}
					{this.renderBlock(tagList[1], "bottom-right")}
				</div>
			</div>
		);
	}
}
