import Icon, { IconSize, IconType } from 'app/common/components/icon/icon';
import SliderSlide from "app/common/components/slider/slide-types/slider-type"
import NoanimationSlide from "app/common/components/slider/slide-types/noanimation-type"
import CarouselSlide from "app/common/components/slider/slide-types/carousel-type"
import cn from 'classnames';
import React from 'react';

import './slider.scss';

export enum sliderAnimationType{
	carousel = "carousel",
	slider = "slider",
	noanimation = "noanimation",
}

interface SliderProps {
	width: string,
	height: string,
	slides: any[],
	overlayManager: boolean,

	endless: boolean,
	autoScroll: number,
	animation: sliderAnimationType,
	transparency: boolean,
}

interface SliderState {
	indexOfActiveSlide: number
}

class Slider extends React.Component<SliderProps, SliderState> {

	static defaultProps = {
		overlayManager: false,

		endless: false,
		autoScroll: 0,
		animation: sliderAnimationType.noanimation,
		transparency: false,
	};

	state = {
		indexOfActiveSlide: 0,
	};

	timer: any = null;

	setActiveSlide = (index: number) => () =>{
		this.startAutoScroll();
		this.setState({
			indexOfActiveSlide: index,
		});
	};

	nextSlide = () => {
		this.startAutoScroll();
		let indexOfActiveSlide: number;

		if (this.props.endless) {
			indexOfActiveSlide = this.state.indexOfActiveSlide < this.props.slides.length - 1? this.state.indexOfActiveSlide + 1: 0;
		}
		else{
	    indexOfActiveSlide = this.state.indexOfActiveSlide < this.props.slides.length - 1? this.state.indexOfActiveSlide + 1: this.state.indexOfActiveSlide;
		}

		this.setState({indexOfActiveSlide})

	};

	prevSlide = () => {
		this.startAutoScroll();
		let indexOfActiveSlide: number;

		if(this.props.endless){
			indexOfActiveSlide = this.state.indexOfActiveSlide > 0? this.state.indexOfActiveSlide - 1: this.props.slides.length - 1
		}
		else{
			indexOfActiveSlide = this.state.indexOfActiveSlide > 0? this.state.indexOfActiveSlide - 1: this.state.indexOfActiveSlide
		}

		this.setState({indexOfActiveSlide})
	};

	startAutoScroll = () => {
		if(this.props.autoScroll && this.props.endless){
			if(this.timer) clearInterval(this.timer)
			this.timer = setInterval( this.nextSlide ,this.props.autoScroll)
		}
	}

	componentDidMount(){
		 this.startAutoScroll()
	}


	render() {
		let size = {
			width: this.props.width,
			height: this.props.height,
		};

		return (
			<div className={cn('slider', this.props.overlayManager ? 'slider_type_overlay' : null)}>

				{
					this.props.animation === "slider" &&
					<SliderSlide 	slides={this.props.slides}
												indexOfActiveSlide = {this.state.indexOfActiveSlide}
												size = {size}
												transparency = {this.props.transparency}/>
				}

				{
					this.props.animation === "noanimation" &&
					<NoanimationSlide slides={this.props.slides}
														indexOfActiveSlide = {this.state.indexOfActiveSlide}
														size = {size}
														transparency = {this.props.transparency}/>
				}

				{
				  this.props.animation === "carousel" &&
					<CarouselSlide  slides={this.props.slides}
													indexOfActiveSlide = {this.state.indexOfActiveSlide}
													size = {size}
													transparency = {this.props.transparency}/>
				}

				<ul className={cn('slider__manager', this.props.overlayManager ? 'slider__manager_type_overlay' : null)}>
					<li
						className={cn('slider__button slider__button_prev', this.state.indexOfActiveSlide === 0 && !this.props.endless? 'slider__button_disabled': null)}
						onClick={this.prevSlide}
					>
						<Icon type={IconType.left} size={this.props.overlayManager ? IconSize.big : IconSize.normal} />
					</li>

					{
						this.props.slides.map((slide, i) => (
							<li
								onClick={this.setActiveSlide(i)}
								key={i}
								className={cn('slider__navigation', this.state.indexOfActiveSlide === i && 'slider__navigation_active')}
							>
								<span className="slider__point"></span>
							</li>
						))
					}

					<li
						className={cn('slider__button', this.state.indexOfActiveSlide === this.props.slides.length - 1 && !this.props.endless? 'slider__button_disabled': null)}
						onClick={this.nextSlide}
					>
						<Icon type={IconType.right} size={this.props.overlayManager ? IconSize.big : IconSize.normal} />
					</li>
				</ul>
			</div>
		);
	}
}

export default Slider;
