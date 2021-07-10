/* eslint-disable jsx-a11y/no-noninteractive-tabindex */
/* eslint-disable jsx-a11y/tabindex-no-positive */
import React, { Component } from "react";
import { PredictionTableData } from "app/common/store/settings/types";
import Icon, { IconSize, IconType } from "app/common/components/icon/icon";
import cn from "classnames";
import "./predictions-container.scss";

interface Props {
	values: PredictionTableData[];
	onDeletePrediction: (index: number) => () => void;
	onChangePredictionsOrder: (indexDrag: number, indexPaste: number) => void;
}

export default class PredictionsContainer extends Component<Props> {
	predictionBlockRef: HTMLDivElement | undefined = undefined;

	predictionBlockDragStart = (e: React.DragEvent<HTMLDivElement>): void => {
		const target = e.target as HTMLDivElement;
		this.predictionBlockRef = target;
		target.style.opacity = "0.25";
	};

	predictionBlockDragEnd = (e: React.DragEvent<HTMLDivElement>): void => {
		const target = e.target as HTMLDivElement;
		target.style.opacity = "1";
	};

	predictionBlockDragOver = (e: React.DragEvent<HTMLDivElement>): void => {
		e.preventDefault();
	};

	predictionBlockDrop = (e: React.DragEvent<HTMLDivElement>): void => {
		if (!this.predictionBlockRef) return;
		let target = e.target as HTMLDivElement;

		const { onChangePredictionsOrder } = this.props;

		while (target.classList[0] !== this.predictionBlockRef.classList[0])
			target = target.parentNode as HTMLDivElement;
		onChangePredictionsOrder(
			Array.from((target.parentNode as HTMLDivElement).children).indexOf(this.predictionBlockRef),
			Array.from((target.parentNode as HTMLDivElement).children).indexOf(target)
		);
	};

	render() {
		const { values, onDeletePrediction } = this.props;

		return (
			<div className="input-predictions-element" onDragOver={this.predictionBlockDragOver}>
				{values.map((item, index) => (
					<div
						key={item.name}
						onDragStart={this.predictionBlockDragStart}
						onDragEnd={this.predictionBlockDragEnd}
						onDrop={this.predictionBlockDrop}
						draggable
						tabIndex={1}
						className={cn("input-predictions-element-block", {
							"input-predictions-element-block_lock": item.is_default,
						})}
					>
						<p className="input-predictions-element-block__position">{item.position}</p>

						<p className="input-predictions-element-block__content">{item.name}</p>

						<button
							type="button"
							className="input-predictions-element-block__button"
							onClick={item.is_default ? undefined : onDeletePrediction(index)}
						>
							<Icon size={IconSize.small} type={item.is_default ? IconType.lock : IconType.close} />
						</button>
					</div>
				))}
			</div>
		);
	}
}
