import { TagCloudGenerator } from "app/common/components/charts/tag-cloud/tag-cloud-generator";
import TermBlock from "app/common/components/charts/tag-cloud/term-block";
import { Tag } from "app/common/components/charts/tag-cloud/types";
import { Terms } from "app/modules/significant-terms/store/types";
import cn from "classnames";
import React from "react";

import "./tag-cloud.scss";

interface IProps {
	tags: Terms;
	className?: string;
	percentage?: boolean;
}

interface IState {
	screenCoefficient: number;
	tagList: Tag[][];
}

export class TagCloud extends React.Component<IProps, IState> {
	constructor(props: IProps) {
		super(props);
		this.state = {
			screenCoefficient: this.getScreenSizeCoefficient(),
			tagList: new TagCloudGenerator().prepare(props.tags),
		};
	}

	getShortVersion(termName: string): string {
		if (termName.length > 9) {
			return `${termName.slice(0, 8)}...`;
		}
		return termName;
	}

	getScreenSizeCoefficient = () => {
		const coeff = 0.9;
		if (window.innerWidth < 1920) return (coeff * window.innerWidth) / 1280;
		return (coeff * 1920) / 1280;
	};

	recalculateScreenCoefficient = () => {
		this.setState({
			screenCoefficient: this.getScreenSizeCoefficient(),
		});
	};

	componentDidMount = () => {
		window.addEventListener("resize", this.recalculateScreenCoefficient);
	};

	componentWillUnmount = () => {
		window.removeEventListener("resize", this.recalculateScreenCoefficient);
	};

	renderBlock = (termsList: Tag[], position: string) => (
		<div className={cn("tag-cloud__block", position)}>
			{termsList.map(({ name, size, absoluteValue, color }, index) => (
				<TermBlock
					key={name}
					shortName={this.getShortVersion(name)}
					name={name}
					value={`${absoluteValue.toFixed(1)}${this.props.percentage ? "%" : ""}`}
					color={color}
					size={size}
					screenCoefficient={this.state.screenCoefficient}
					zIndex={index}
				/>
			))}
		</div>
	);

	render() {
		const { tagList } = this.state;

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
