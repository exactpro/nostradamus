import { Keywords, PredictMetricsName } from "app/modules/predict-text/predict-text";
import React, { ReactElement } from "react";

import "./backlight-textarea.scss";

interface Props {
	text: string;
	keywords: Keywords | undefined;
	layoutArr: PredictMetricsName[];
	disabled?: boolean;
	onChangeText: (text: string) => void;
}

class BacklightTextArea extends React.Component<Props> {
	backdropContainerRef: React.RefObject<HTMLDivElement>;
	textareaPlaceholder = "Copy or type your description here";

	constructor(props: Props) {
		super(props);

		this.backdropContainerRef = React.createRef();
	}

	syncScroll = () => {
		if (this.backdropContainerRef.current) {
			const { scrollTop } = this.backdropContainerRef.current
				.getElementsByClassName("backlight-textarea__textarea")
				.item(0) as Element;

			const texts = this.backdropContainerRef.current.getElementsByClassName(
				"backlight-textarea__text"
			);

			// @ts-ignore
			// eslint-disable-next-line no-restricted-syntax
			for (const text of texts) {
				(text as Element).scrollTop = scrollTop;
			}
		}
	};

	onChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
		this.props.onChangeText(e.target.value);
	};

	componentDidUpdate() {
		// need do, after appearing new term
		this.syncScroll();
	}

	getColor = (metric: PredictMetricsName) => {
		switch (metric) {
			case "Priority":
				return "yellow";
			case "resolution":
				return "red";
			case "areas_of_testing":
				return "purple";
		}
	};

	addBacklight = (text: string, keywords?: Keywords) => {
		const res: any[] = [];
		if (keywords) {
			this.props.layoutArr.forEach((metric) => {
				keywords[metric].forEach((word) => {
					res.push(wrapSubstrToColor(text, word, this.getColor(metric)));
				});
			});
		}

		return res.length ? res : [text];
	};

	render() {
		return (
			<div className="backlight-textarea">
				<div className="backlight-textarea__backdrop" ref={this.backdropContainerRef}>
					{this.addBacklight(this.props.text, this.props.keywords).map((text, index) => (
						<pre key={index} className="backlight-textarea__text">
							{text || (
								<span className="backlight-textarea__placeholder">{this.textareaPlaceholder}</span>
							)}
						</pre>
					))}

					<textarea
						onScroll={this.syncScroll}
						className="backlight-textarea__textarea"
						value={this.props.text}
						onChange={this.onChange}
						disabled={this.props.disabled}
						placeholder="Copy or type your description here"
					>
						{/* text area */}
					</textarea>
				</div>
			</div>
		);
	}
}

export default BacklightTextArea;

function wrapSubstrToColor(text: string, substr: string, color: string) {
	const splitText: ReactElement[] = [];

	const find = () => {
		return text.toLowerCase().indexOf(substr.toLocaleLowerCase());
	};

	let key = 0;
	while (find() > -1) {
		const startPos = find();
		splitText.push(
			<React.Fragment key={key + 1}>{text.slice(0, startPos)}</React.Fragment>,
			<span key={key + 2} className={`color-${color}`}>
				{text.slice(startPos, startPos + substr.length)}
			</span>
		);
		// eslint-disable-next-line no-param-reassign
		text = text.slice(startPos + substr.length);
		key += 2;
	}

	splitText.push(<React.Fragment key={key + 1}>{text}</React.Fragment>);

	return splitText;
}
