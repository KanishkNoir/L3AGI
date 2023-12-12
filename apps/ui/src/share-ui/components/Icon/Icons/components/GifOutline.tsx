/* eslint-disable */
/* tslint:disable */
import * as React from 'react';
export interface GifOutlineProps extends React.SVGAttributes<SVGElement> {
size?: string | number;
}
const GifOutline: React.FC<GifOutlineProps> = ({size, ...props}) => (
  <svg viewBox="0 0 40 40" fill="currentColor" width={ size || "40" } height={ size || "40" } {...props}>
    <g filter="url(#filter0_bd_718_13950)" fill="#fff">
      <path d="M20.875 13C20.6429 13 20.4204 13.0922 20.2563 13.2563 20.0922 13.4204 20 13.6429 20 13.875V26.125C20 26.3571 20.0922 26.5796 20.2563 26.7437 20.4204 26.9078 20.6429 27 20.875 27 21.1071 27 21.3296 26.9078 21.4937 26.7437 21.6578 26.5796 21.75 26.3571 21.75 26.125V13.875C21.75 13.6429 21.6578 13.4204 21.4937 13.2563 21.3296 13.0922 21.1071 13 20.875 13zM30.9375 13H25.6875C25.4554 13 25.2329 13.0922 25.0688 13.2563 24.9047 13.4204 24.8125 13.6429 24.8125 13.875V26.125C24.8125 26.3571 24.9047 26.5796 25.0688 26.7437 25.2329 26.9078 25.4554 27 25.6875 27 25.9196 27 26.1421 26.9078 26.3062 26.7437 26.4703 26.5796 26.5625 26.3571 26.5625 26.125V20.875H29.625C29.8571 20.875 30.0796 20.7828 30.2437 20.6187 30.4078 20.4546 30.5 20.2321 30.5 20 30.5 19.7679 30.4078 19.5454 30.2437 19.3813 30.0796 19.2172 29.8571 19.125 29.625 19.125H26.5625V14.75H30.9375C31.1696 14.75 31.3921 14.6578 31.5562 14.4937 31.7203 14.3296 31.8125 14.1071 31.8125 13.875 31.8125 13.6429 31.7203 13.4204 31.5562 13.2563 31.3921 13.0922 31.1696 13 30.9375 13zM16.5 19.125H13.875C13.6429 19.125 13.4204 19.2172 13.2563 19.3813 13.0922 19.5454 13 19.7679 13 20 13 20.2321 13.0922 20.4546 13.2563 20.6187 13.4204 20.7828 13.6429 20.875 13.875 20.875H15.625V22.625C15.625 23.3212 15.3484 23.9889 14.8562 24.4812 14.3639 24.9734 13.6962 25.25 13 25.25 12.3038 25.25 11.6361 24.9734 11.1438 24.4812 10.6516 23.9889 10.375 23.3212 10.375 22.625V17.375C10.3751 16.7361 10.6082 16.1192 11.0306 15.6398 11.453 15.1604 12.0356 14.8515 12.6694 14.771 13.3032 14.6904 13.9447 14.8437 14.4735 15.2021 15.0024 15.5606 15.3825 16.0996 15.5424 16.7181 15.571 16.8295 15.6212 16.9342 15.6902 17.0261 15.7592 17.1181 15.8457 17.1955 15.9447 17.2541 16.0436 17.3126 16.1532 17.351 16.267 17.3672 16.3809 17.3833 16.4968 17.3769 16.6081 17.3482 16.7195 17.3196 16.8241 17.2693 16.916 17.2001 17.0078 17.131 17.0852 17.0445 17.1436 16.9454 17.202 16.8464 17.2404 16.7368 17.2564 16.623 17.2724 16.5091 17.2659 16.3932 17.2371 16.2819 16.9709 15.2508 16.3378 14.3521 15.4565 13.7543 14.5751 13.1565 13.506 12.9007 12.4495 13.0348 11.3931 13.1689 10.4218 13.6837 9.7177 14.4827 9.01362 15.2817 8.62512 16.3101 8.625 17.375V22.625C8.625 23.7853 9.08594 24.8981 9.90641 25.7186 10.7269 26.5391 11.8397 27 13 27 14.1603 27 15.2731 26.5391 16.0936 25.7186 16.9141 24.8981 17.375 23.7853 17.375 22.625V20C17.375 19.768 17.2828 19.5454 17.1187 19.3813 16.9546 19.2172 16.7321 19.125 16.5 19.125z"
      />
    </g>
    <defs>
      <filter id="filter0_bd_718_13950" x="-10" y="-10" width="60" height="60" filterUnits="userSpaceOnUse" colorInterpolationFilters="sRGB">
        <feFlood result="BackgroundImageFix" floodOpacity="0" />
        <feGaussianBlur in="BackgroundImageFix" stdDeviation="5" />
        <feComposite in2="SourceAlpha" operator="in" result="effect1_backgroundBlur_718_13950" />
        <feColorMatrix in="SourceAlpha" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha" />
        <feOffset dy="1" />
        <feGaussianBlur stdDeviation="1.5" />
        <feColorMatrix values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.2 0" />
        <feBlend in2="effect1_backgroundBlur_718_13950" result="effect2_dropShadow_718_13950" />
        <feBlend in="SourceGraphic" in2="effect2_dropShadow_718_13950" result="shape" />
      </filter>
    </defs>
  </svg>
);
GifOutline.displayName = 'GifOutline';
export default GifOutline;
/* tslint:enable */
/* eslint-enable */