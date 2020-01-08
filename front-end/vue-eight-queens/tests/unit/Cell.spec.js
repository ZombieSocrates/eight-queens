import { shallowMount } from '@vue/test-utils'
import Cell from '@/components/Cell'

describe('Cell', () => {
  const wrapper = shallowMount(Cell, {
	  setData: {
		  hasQueen: true,
		  cellStyle: {
		  	backgroundColor: '#000000'
		  }
	  }
  })
  it('changes color when clicked on, if it has a queen', () => {
      const baseColor = wrapper.vm.cellStyle.backgroundColor
      console.log(baseColor)
	  wrapper.trigger('click')
	  expect(wrapper.element.style['background-color']).not.toBe(baseColor)
  })
})