import React, { ReactElement } from "react";
import Slider, { sliderAnimationType } from "app/common/components/slider/slider";

import "./auth-page-slider.scss";

import slide0 from "assets/images/auth-page/slides/slider_slide1.png";
import slide1 from "assets/images/auth-page/slides/slider_slide2.png";

interface ISlide {
	slideImage: string;
	slideTitle: string;
	slidePlainText: string;
	slideDisorderedList: string[];
}

class AuthPageSlider extends React.PureComponent {
	slide = (index: number): ReactElement => {
		let slide: ISlide;

		switch (index) {
			case 0:
				slide = {
					slideImage: slide0,
					slideTitle: "Create High-Quality Bug Reports",
					slidePlainText: "Verify the quality of your bug reports by getting predictions of:",
					slideDisorderedList: [
						"priority levels",
						"a bug being rejected",
						"a bug being fixed, including time to resolve",
						"a bug belonging to a specific area of testing",
					],
				};
				break;
			default:
				slide = {
					slideImage: slide1,
					slideTitle: "Project Management Made Easy",
					slidePlainText: "",
					slideDisorderedList: [
						"evaluate your team's performance",
						"discover dependencies hidden in development and testing",
					],
				};
				break;
		}

		const style = {
			backgroundImage: `url(${slide.slideImage})`,
		};

		return (
			<div className="auth-page__slide auth-page-slide" style={style}>
				{slide.slideTitle && <h4 className="auth-page-slide__title">{slide.slideTitle}</h4>}

				{slide.slidePlainText && (
					<p className="auth-page-slide__plain-text">{slide.slidePlainText}</p>
				)}

				<ul className="auth-page-slide__disordered-list">
					{slide.slideDisorderedList.map((value) => (
						<li className="auth-page-slide__disordered-list-elem" key={value}>
							{value}
						</li>
					))}
				</ul>
			</div>
		);
	};

	render(): ReactElement {
		const slides = new Array(2).fill(0);

		return (
			<Slider
				width="100%"
				height="100%"
				overlayManager
				animation={sliderAnimationType.slider}
				endless
				autoScroll={30000}
				slides={slides.map((elem, index: number) => this.slide(index))}
			/>
		);
	}
}

export default AuthPageSlider;
