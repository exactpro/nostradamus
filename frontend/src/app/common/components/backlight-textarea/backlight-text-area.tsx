import { Keywords } from 'app/modules/predict-text/predict-text';
import React from 'react';

import './backlight-textarea.scss';

interface Props {
	text: string,
	keywords: Keywords | undefined,
	disabled?: boolean,
	onChangeText: (text: string) => void
}

class BacklightTextArea extends React.Component<Props> {

	backdropContainerRef: React.RefObject<HTMLDivElement>;

	constructor(props: Props) {
		super(props);

		this.backdropContainerRef = React.createRef();
	}

	syncScroll = () => {
		if (this.backdropContainerRef.current) {
			let scrollTop = (this.backdropContainerRef.current
				.getElementsByClassName('backlight-textarea__textarea')
				.item(0) as Element)
				.scrollTop;

			let texts = this.backdropContainerRef.current
				.getElementsByClassName('backlight-textarea__text');

			// @ts-ignore
			for (let text of texts) {
				(text as Element).scrollTop = scrollTop;
			}
		}
	};

	onChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
		this.props.onChangeText(e.target.value);
	};

	addBacklight = (text: string, keywords?: Keywords): string[] => {
		let result: string[] = [];

		if (keywords) {
			keywords.resolution.forEach((keyword) => {
				result.push(wrapSubstrToColor(text, keyword, 'red'));
			});

			keywords.Priority.forEach((keyword) => {
				result.push(wrapSubstrToColor(text, keyword, 'yellow'));
			});

			keywords.areas_of_testing.forEach((keyword) => {
				result.push(wrapSubstrToColor(text, keyword, 'purple'));
			});

			return result.length ? result : [ text ];
		} else {
			return [ text ];
		}
	};

	render() {
		return (
			<div className="backlight-textarea">

				<div className="backlight-textarea__backdrop" ref={this.backdropContainerRef}>
					{
						this.addBacklight(this.props.text, this.props.keywords).map((text, index) => (
							<pre
								key={index}
								className="backlight-textarea__text"
								dangerouslySetInnerHTML={{ __html: text }}
							>{/*text area text*/}</pre>
						))
					}

					<textarea
						onScroll={this.syncScroll}
						className="backlight-textarea__textarea"
						value={this.props.text}
						onChange={this.onChange}
						disabled={this.props.disabled}
					>{/*text area*/}</textarea>
				</div>
			</div>
		);
	}

}

export default BacklightTextArea;

function wrapSubstrToColor(text: string, substr: string, color: string) {
	let splitText = [];

	let find = () => {
		return text.toLowerCase().indexOf(substr.toLocaleLowerCase());
	};

	while (find() > -1) {
		let startPos = find();
		splitText.push(
			text.slice(0, startPos),
			`<span class="color-${color}">${text.slice(startPos, startPos + substr.length)}</span>`,
		);

		text = text.slice(startPos + substr.length);
	}

	splitText.push(text);

	return splitText.join('');
}
