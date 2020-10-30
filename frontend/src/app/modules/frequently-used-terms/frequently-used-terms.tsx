import React, { ReactElement, RefObject } from "react";

import Slider from "app/common/components/slider/slider";

import "./frequently-used-terms.scss";

const ONE_ROW_HEIGHT = 29;

interface FrequentlyUsedTermsState {
	slides: unknown[];
	rowPerSlide: number;
	slideHeight: number;
}

interface FrequentlyUsedTermsProps {
	frequentlyTermsList: string[];
}
	
class FrequentlyUsedTerms extends React.Component<
	FrequentlyUsedTermsProps,
	FrequentlyUsedTermsState
> {
	myRef: RefObject<HTMLDivElement>;

	constructor(props: FrequentlyUsedTermsProps) {
		super(props);

		this.myRef = React.createRef();

		this.state = {
			slides: [],
			rowPerSlide: 1,
			slideHeight: ONE_ROW_HEIGHT,
		};
	}

	private get containerHeight() {
		if (this.myRef.current && this.myRef.current.parentNode) {
			return this.myRef.current.closest("section")!.getBoundingClientRect().height - 100 || 0;
		}
		return 0;
	}

	componentDidMount(): void {
		window.addEventListener("resize", this.onResizeWindow);
		const { slides } = this.state;

		if (!slides.length) {
			this.generateSlidePage();
			this.forceUpdate();
		}
	}

	componentDidUpdate(): void {
		const { slides } = this.state;

		if (!slides.length) {
			this.generateSlide();
		}
	}

	componentWillUnmount(): void {
		window.removeEventListener("resize", this.onResizeWindow);
	}

	generateSlidePage = () => {
		const rowPerSlide = Math.round(this.containerHeight / ONE_ROW_HEIGHT);
		const slideHeight = ONE_ROW_HEIGHT * rowPerSlide; 
		
		this.setState({rowPerSlide, slideHeight})
	};

	generateSlide = (): void => {
		if (this.myRef.current) {
			this.generateSlidePage();
			const rowCount = this.myRef.current.offsetHeight / ONE_ROW_HEIGHT;

			const slidesCount: number = Math.ceil(rowCount / this.state.rowPerSlide);
			const slides: unknown[] = [];

			for (let i = 0; i < slidesCount; i += 1) {
				slides.push(this.renderTerms(i)());
			}

			this.setState({ slides });
		}
	};

	onResizeWindow = (): void => {
		this.generateSlide();
	};

	renderTerms = (index: number) => (): ReactElement => {
		const { frequentlyTermsList } = this.props;
		const {slideHeight} = this.state;

		const style = {
			marginTop: `${slideHeight * index * -1}px`,
		};

		return (
			<div className="wrapper" style={style}>
				{frequentlyTermsList.map((word) => (
					<div className="word" key={word}>
						{word}
					</div>
				))}
			</div>
		);
	};

	render(): ReactElement {
		const { frequentlyTermsList } = this.props;
		const { slides, slideHeight } = this.state;

		return (
			<>
				<div className="helper">
					<div className="wrapper" ref={this.myRef}>
						{frequentlyTermsList.map((word) => (
							<div className="word" key={word}>
								{word}
							</div>
						))}
					</div>
				</div>

				<Slider width="100%" height={`${slideHeight}px`} slides={slides} />
			</>
		);
	}
}

export default FrequentlyUsedTerms;
